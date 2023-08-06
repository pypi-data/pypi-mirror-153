import pkgutil
from pathlib import Path
from textwrap import dedent
from typing import Dict, Optional, Tuple

from sym.shared.cli.helpers import os
from sym.shared.cli.helpers.contexts import push_envs
from sym.shared.cli.helpers.tee import Tee

from sym.cli.constants.env import (
    ANSIBLE_CONNECTION_PLUGINS,
    ANSIBLE_DEBUG,
    ANSIBLE_PIPELINING,
    ANSIBLE_SSH_ARGS,
    ANSIBLE_SSH_ARGS_DEBUG,
    ANSIBLE_SSH_ARGS_NO_CONTROL_MASTER,
    ANSIBLE_SSH_EXECUTABLE,
    ANSIBLE_SSH_RETRIES,
    DEFAULT_ANSIBLE_SSH_ARGS,
    DEFAULT_ANSIBLE_SSH_RETRIES,
    ENABLED,
    OBJC_DISABLE_INITIALIZE_FORK_SAFETY,
    YES,
)
from sym.cli.helpers.boto import get_identity
from sym.cli.helpers.config import SymConfigFile
from sym.cli.helpers.params import get_ansible_user
from sym.cli.saml_clients.aws_profile import AwsCredentialsPath, AwsProfile
from sym.cli.saml_clients.saml_client import SAMLClient

from ..ansible import connection
from ..helpers.ssh import ssh_key_and_config
from ..version import __version__

ANSIBLE_SSH_PATH = "ansible/ssh"
ANSIBLE_SSH_PROFILE = "sym-ansible"

AWS_SSM_PATH = f"ansible/connection/{__version__}/sym_aws_ssm.py"

BUCKET_PREFIX = "sym-ansible-"
BUCKET_REGION = "us-east-1"


def get_ansible_bucket_name(client: SAMLClient) -> str:
    return client.get_profile().ansible_bucket or get_default_ansible_bucket_name(client)


def get_default_ansible_bucket_name(client: SAMLClient) -> str:
    account = get_identity(client)["Account"]
    return f"{BUCKET_PREFIX}{account}"


def get_ansible_ssh_profile(client: SAMLClient):
    return f"{ANSIBLE_SSH_PROFILE}-{client.resource}"


def aws_ssm_connection_plugin() -> Path:
    file = SymConfigFile(file_name=AWS_SSM_PATH, uid_scope=False)
    if not file.path.exists():
        try:
            file.put(
                pkgutil.get_data(connection.__name__, file.path.name).decode("utf-8")
            )
        except:
            # PyOxidizer doesn't retain source files in some cases,
            # so fall back to a (hopefully up-to-date) hard-coded source.
            file.put(connection.sym_aws_ssm_source)
    return file.path


def ansible_connection_plugins_value() -> str:
    plugin = aws_ssm_connection_plugin()
    return ":".join(
        [
            str(plugin.parent),
            "~/.ansible/plugins/connection",  # these are the defaults
            "/usr/share/ansible/plugins/connection",
        ]
    )


def ansible_profile_proxy(client):
    return client.clone(klass=AwsProfile, resource=get_ansible_ssh_profile(client))


def sym_subcommand(client, subcommand, args="") -> str:
    proxy_client = ansible_profile_proxy(client)
    return f"sym {proxy_client.cli_options} {subcommand} {proxy_client.resource} {args}"


def create_ssh_bin(client):
    proxy_client = ansible_profile_proxy(client)
    ssh_bin = proxy_client.subconfig(ANSIBLE_SSH_PATH)

    command = sym_subcommand(client, "ssh", '"$@"')
    if log_dir := client.options.log_dir:
        command = Tee.tee_command(log_dir, command)

    # fmt: off
    ssh_bin.put(dedent(
        f"""
        #!/bin/bash

        export PYTHONUNBUFFERED=1

        {command}
        """
    ).lstrip())
    # fmt: on
    ssh_bin.path.chmod(0o755)
    return ssh_bin


def get_ansible_env(
    ssh_bin: str,
    *,
    debug: bool = False,
    control_master: bool = True,
) -> Dict:
    envs = {
        ANSIBLE_SSH_EXECUTABLE: ssh_bin,
        ANSIBLE_SSH_RETRIES: DEFAULT_ANSIBLE_SSH_RETRIES,
        ANSIBLE_PIPELINING: ENABLED,
    }
    if debug:
        envs[ANSIBLE_SSH_ARGS] = ANSIBLE_SSH_ARGS_DEBUG
        envs[ANSIBLE_DEBUG] = ENABLED
    elif not control_master:
        envs[ANSIBLE_SSH_ARGS] = ANSIBLE_SSH_ARGS_NO_CONTROL_MASTER
    else:
        envs[ANSIBLE_SSH_ARGS] = DEFAULT_ANSIBLE_SSH_ARGS

    return envs


def get_send_command_args(client: SAMLClient, ssm_timeout: int):
    bucket_name = get_ansible_bucket_name(client)
    client.dprint(f"Using bucket s3://{bucket_name}")

    sym_host_to_instance_cmd = sym_subcommand(
        client,
        "host-to-instance",
        "$HOST --json",
    )
    extra_vars = {
        "ansible_aws_ssm_bucket": bucket_name,
        "ansible_aws_ssm_host_cmd": sym_host_to_instance_cmd,
        "ansible_aws_ssm_region": BUCKET_REGION,
        "ansible_aws_ssm_profile": get_ansible_ssh_profile(client),
        "ansible_aws_ssm_timeout": str(ssm_timeout),
    }
    return " ".join(f"{k}='{v}'" for k, v in extra_vars.items())


def run_ansible(
    client: SAMLClient,
    command: Tuple[str, ...],
    *,
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
    forks: int,
    ssm_timeout: int,
    binary: str = "ansible",
    control_master: bool = True,
    send_command: bool = False,
):
    client.dprint(f"creating SSH artifacts")

    ssh_bin = str(create_ssh_bin(client))
    ssh_key, _ = ssh_key_and_config(client)
    args = [
        binary,
        f"--user={get_ansible_user()}",
        f"--private-key={ssh_key}",
        f"--scp-extra-args=-S '{ssh_bin}'",
        f"--sftp-extra-args=-S '{ssh_bin}'",
        *command,
    ]

    envs = get_ansible_env(ssh_bin, debug=client.debug, control_master=control_master)

    if send_command:
        envs[OBJC_DISABLE_INITIALIZE_FORK_SAFETY] = YES
        envs[ANSIBLE_CONNECTION_PLUGINS] = ansible_connection_plugins_value()

        args.append("--connection=sym_aws_ssm")
        args.append(f"--forks={forks}")
        args.append(f"--extra-vars={get_send_command_args(client, ssm_timeout)}")
    else:
        # Sometimes Ansible tries to use Paramiko instead of native SSH
        args.append("--connection=ssh")

    if client.debug:
        args.append("-vvvv")

    if client.log_dir:
        envs["ANSIBLE_LOG_PATH"] = str(Tee.path_for_fd(client.log_dir, "ansible"))
    client.write_creds(path=AwsCredentialsPath, profile=get_ansible_ssh_profile(client))

    if ansible_aws_profile:
        ansible_client: AwsProfile = client.clone(
            klass=AwsProfile, resource=ansible_aws_profile
        )
        ansible_client.raise_if_invalid()
    elif ansible_sym_resource:
        ansible_client = client.clone(resource=ansible_sym_resource)
    else:
        ansible_client = client

    client.dprint(f"ansible: client='{ansible_client._cli_options()}', envs={envs}")

    with push_envs(envs):
        os.execvp(ansible_client, args)
