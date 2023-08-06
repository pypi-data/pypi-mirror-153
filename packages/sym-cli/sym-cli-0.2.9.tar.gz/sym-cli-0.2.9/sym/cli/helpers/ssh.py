import os
import re
import subprocess
import sys
from datetime import timedelta
from pathlib import Path
from signal import SIG_IGN, SIGINT, SIGPIPE, SIGTSTP, signal
from subprocess import CalledProcessError
from textwrap import dedent
from typing import List, Sequence, Tuple

import click
from sym.shared.cli.helpers.contexts import push_env, push_envs

from sym.cli.decorators import intercept_errors, retry, run_subprocess
from sym.cli.errors import (
    AccessDenied,
    FailedSubprocessError,
    MissingPublicKey,
    SuppressedError,
    TargetNotConnected,
    WrappedSubprocessError,
    raise_if_match,
)
from sym.cli.helpers.boto import (
    AccessDeniedPattern,
    TargetNotConnectedPattern,
    send_ssh_key,
    ssm_interactive_command,
    ssm_ssh_session,
)
from sym.cli.helpers.config import Config, SymConfigFile
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.params import get_ssh_user
from sym.cli.helpers.sym_group import SymGroup
from sym.cli.saml_clients.saml_client import SAMLClient

MissingPublicKeyPattern = re.compile(r"Permission denied \(.*publickey.*\)")
ConnectionClosedPattern = re.compile(r"Connection to .* closed")

AWS_ERROR_PATTERNS = {
    TargetNotConnectedPattern: TargetNotConnected,
    AccessDeniedPattern: AccessDenied,
}

SSHConfigPath = "ssh/config"
SSHKeyPath = "ssh/key"

OPENSSH_VERSION_PATTERN = re.compile(r"OpenSSH_(\d)\.(\d)")
MIN_VER_FOR_CONTROL_MASTER = (8, 1)


def check_ssh_version() -> bool:
    ssh_ok = get_ssh_version() >= MIN_VER_FOR_CONTROL_MASTER
    if not ssh_ok:
        click.secho(
            "OpenSSH version is out of date, control master will be disabled.",
            fg="yellow",
        )
        version = ".".join(map(str, MIN_VER_FOR_CONTROL_MASTER))
        click.secho(
            f"This will negatively affect performance, please consider upgrading to OpenSSH {version}+.",
            fg="yellow",
        )
    return ssh_ok


def get_ssh_version() -> Tuple[int, int]:
    result = subprocess.run(["ssh", "-V"], text=True, capture_output=True).stderr
    if match := OPENSSH_VERSION_PATTERN.search(result):
        return tuple(map(int, (match[1], match[2])))
    return (0, 0)


def ssh_key_and_config(client: SAMLClient):
    ssh_key = SymConfigFile(file_name=SSHKeyPath, uid_scope=False)
    ssh_config = client.subconfig(SSHConfigPath, ssh_key=str(ssh_key))
    return (ssh_key, ssh_config)


@intercept_errors()
@run_subprocess
def _gen_ssh_key(dest: SymConfigFile):
    with dest.exclusive_create() as f:
        Path(f.name).unlink(missing_ok=True)
        yield "ssh-keygen", {"t": "rsa", "f": f.name, "N": ""}


def gen_ssh_key(dest: SymConfigFile, options: GlobalOptions):
    try:
        _gen_ssh_key(
            dest,
            capture_output_=True,
            input_="n\n",
            run_subprocess_options_=options,
            intercept_errors_options_=options,
        )
    except FailedSubprocessError:
        if not dest.path.exists():
            raise


def maybe_gen_ssh_key(client):
    ssh_key, _ = ssh_key_and_config(client)
    if not ssh_key.path.exists():
        gen_ssh_key(ssh_key, client.options)


def ssh_tunnel_opts(client) -> dict:
    _, ssh_config = ssh_key_and_config(client)
    return {
        "F": str(ssh_config),
        "v": client.debug,
    }


def ssh_args(client, instance, port) -> tuple:
    opts = {"p": str(port), "l": get_ssh_user(), **ssh_tunnel_opts(client)}
    return ("ssh", instance, opts, {"o": f"HostKeyAlias={instance}"})


@run_subprocess
def _start_background_ssh_session(client: SAMLClient, instance: str, port: int, *command):
    with push_envs({"SHELL": "/bin/bash", "SYM_SKIP_ENSURE_KEY": "1"}):
        yield (
            *ssh_args(client, instance, port),
            {"f": True},
            {"o": "BatchMode=yes"},
            *command,
        )


@run_subprocess
def _start_ssh_session(client: SAMLClient, instance: str, port: int, *command: str):
    with push_envs({"SHELL": "/bin/bash", "SYM_SKIP_ENSURE_KEY": "1"}):
        yield (*ssh_args(client, instance, port), *command)


@intercept_errors(AWS_ERROR_PATTERNS, suppress=True)
@run_subprocess
def _start_ssh_tunnel(client: SAMLClient, program: str, *opts: str):
    with push_env("SHELL", "/bin/bash"):
        yield (program, ssh_tunnel_opts(client), *opts)


@intercept_errors(suppress=True)
@run_subprocess
def raw_ssh(*args):
    yield ("ssh", *args)


def _parse_options_from_args(args: Sequence[str]):
    opts = {}
    for i, arg in enumerate(args):
        if arg == "-o" and i + 1 < len(args):
            k, v = re.split(r"=|\s+", args[i + 1])
            opts[k.casefold()] = (v, i)
    return opts


def _on_ssh_error(client: SAMLClient, instance: str, args: Sequence[str]):
    """
    When there's an SSH error, we'll update our config to indicate we have an error in the
    instance and we'll attempt to clear out any existing control path files.
    """
    Config.touch_instance(instance, error=True)
    opts = _parse_options_from_args(args)
    if vi := opts.get("controlpath"):
        try:
            os.unlink(vi[0])
        except OSError as err:
            client.dprint(f"Error cleaning up controlpath: {err}")


def _preprocess_args(client: SAMLClient, instance: str, args: Sequence[str]) -> List[str]:
    """
    Checks the instance to make sure there is an existing SSH key that was used within the TTL. If not,
    delete the ControlMaster and ControlPath arguments. Attempting to use an invalid ControlPath may
    cause the SSH client to hang.
    """
    processed = list(args)
    opts = _parse_options_from_args(args)
    if not Config.check_instance_ttl(instance):
        for opt in ("controlmaster", "controlpath"):
            if vi := opts.get(opt):
                del processed[vi[1] : vi[1] + 2]

        processed.extend(["-o", "ControlMaster=no"])
        client.dprint("removed controlpath from ssh args")
    return processed


def start_ssh_tunnel(client: SAMLClient, program: str, opts: Sequence[str]):
    ensure_ssh_config(client)
    client.dprint("starting SSH tunnel")
    _start_ssh_tunnel(client, program, *opts)


@retry(TargetNotConnected, delay=1, count=2)
@retry(MissingPublicKey, delay=0, count=2)
def start_ssh_session(
    client: SAMLClient,
    instance: str,
    port: int,
    *,
    args: Sequence[str] = [],
    command: Sequence[str] = [],
    wrap: bool = True,
):
    args = _preprocess_args(client, instance=instance, args=args)
    ensure_ssh_key(client, instance, port)
    client.dprint("starting SSH session")
    try:
        _start_ssh_session(client, instance, port, *args, *command)
    except CalledProcessError as err:
        if ConnectionClosedPattern.search(err.stderr):
            raise SuppressedError(err, echo=True) from err
        client.dprint(f"SSH Session Error: {err.stderr}")
        _on_ssh_error(client, instance, args=args)
        if MissingPublicKeyPattern.search(err.stderr):
            raise MissingPublicKey(err, get_ssh_user()) from err

        # If the ssh key path is cached then this doesn't get intercepted in ensure_ssh_key
        raise_if_match(AWS_ERROR_PATTERNS, err.stderr)

        if wrap:
            raise WrappedSubprocessError(
                err, f"Contact your Sym administrator.", report=True
            ) from err
        else:
            raise SuppressedError(err, echo=True)
    else:
        Config.touch_instance(instance)


def gen_local_ssh_config(client) -> SymConfigFile:
    client.dprint("writing SSH key")
    ssh_key, ssh_config = ssh_key_and_config(client)
    sym_cmd = f"PYTHONUNBUFFERED=1 sym {client.cli_options} ssh-session {client.resource} --instance %h --port %p"

    if client.debug:
        mux_config = f"""
            ControlMaster no
        """
    else:
        mux_config = f"""
            ControlMaster auto
        """

    # fmt: off
    ssh_config.put(dedent(  # Ensure the SSH Config first, always
        f"""
        Host *
            IdentityFile {str(ssh_key)}
            IdentitiesOnly yes
            PreferredAuthentications publickey
            PubkeyAuthentication yes
            StrictHostKeyChecking no
            PasswordAuthentication no
            ChallengeResponseAuthentication no
            GSSAPIAuthentication no
            ProxyCommand sh -c "{sym_cmd} || exit \\$?"
            {mux_config.strip()}
        """
    ))
    # fmt: on
    return ssh_config


@retry(TargetNotConnected, delay=1, count=2)
@intercept_errors(AWS_ERROR_PATTERNS, suppress=True)
def ensure_public_key_on_instance(
    client,
    instance: str,
    port: int,
    *,
    args: Sequence[str] = [],
    ttl: timedelta = timedelta(days=1),
):
    if Config.check_instance_ttl(instance, ttl):
        client.dprint(f"Skipping remote SSH key check for {instance}")
        return

    try:
        _start_background_ssh_session(
            client, instance, port, *args, "exit", capture_output_=True
        )
    except CalledProcessError as err:
        client.dprint(f"SSH Check Error: {err.stdout}")
        if not MissingPublicKeyPattern.search(err.stderr):
            raise
        ssh_key, _ = ssh_key_and_config(client)
        send_ssh_key(client, instance, ssh_key)
    else:
        client.dprint("remote SSH key check succeeded")
        Config.touch_instance(instance)


def ensure_ssh_config(client):
    gen_local_ssh_config(client)
    maybe_gen_ssh_key(client)


def ensure_ssh_key(client, instance: str, port: int):
    ensure_ssh_config(client)
    ensure_public_key_on_instance(client, instance, port)


def _set_handlers(instance):
    def pipe_handler(signum, frame):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        # Set error state on session end.
        # If the connection was actually successful,
        # the parent thread will re-set a success state.
        # This is the only reliable way to avoid error
        # loops with Ansible due to missing SSH public keys.
        Config.touch_instance(instance, error=True)

    signal(SIGPIPE, pipe_handler)
    signal(SIGINT, SIG_IGN)
    signal(SIGTSTP, SIG_IGN)


def start_tunnel(client, instance: str, port: int):
    client.dprint("execing aws ssm")
    SymGroup.reset_tees()
    _set_handlers(instance)

    with ssm_ssh_session(client, instance, port) as command:
        client.exec(*command, suppress_=True)


def start_interactive_command(client, instance: str, command: Sequence[str]):
    client.dprint("execing aws ssm interactive command")
    SymGroup.reset_tees()
    _set_handlers(instance)

    with ssm_interactive_command(client, instance, get_ssh_user(), command) as command:
        client.exec(*command, suppress_=True)
