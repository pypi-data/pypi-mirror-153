import re
import sys
from typing import Dict, Optional, Sequence

import click
from sym.shared.cli.helpers.keywords_to_options import keywords_to_options

from sym.cli.decorators import command_require_bins, loses_interactivity, require_login
from sym.cli.helpers.ec2.factory import get_ec2_client
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from ..helpers.options import resource_argument
from ..helpers.ssh import raw_ssh, start_interactive_command, start_ssh_session
from .sym import sym

SSH_MAN = """
     ssh [-AaCfGgKkMNnqsTtVvXxYy] [-B bind_interface] [-b bind_address] [-c cipher_spec]
         [-D [bind_address:]port] [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
         [-i identity_file] [-J jump_destination] [-L address] [-l login_name] [-m mac_spec] [-O ctl_cmd]
         [-o option] [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
         [-w local_tun[:remote_tun]] destination [command]
"""

SSH_OPTS = list(
    map(
        lambda x: x.casefold(),
        {
            "LogLevel",
            "CheckHostIP",
            "ForwardX11Trusted",
            "HostKeyAlias",
            "SetEnv",
            "UpdateHostKeys",
            "ClearAllForwardings",
            "GSSAPIKeyExchange",
            "HashKnownHosts",
            "remote_tun",
            "CertificateFile",
            "Hostname",
            "RemoteForward",
            "PubkeyAuthentication",
            "HostbasedKeyTypes",
            "AddKeysToAgent",
            "NumberOfPasswordPrompts",
            "KbdInteractiveDevices",
            "BatchMode",
            "PubkeyAcceptedKeyTypes",
            "CASignatureAlgorithms",
            "LocalCommand",
            "GSSAPIClientIdentity",
            "UserKnownHostsFile",
            "CanonicalizePermittedCNAMEs",
            "PermitLocalCommand",
            "HostName",
            "VerifyHostKeyDNS",
            "UsePrivilegedPort",
            "AddressFamily",
            "RemoteCommand",
            "HostKeyAlgorithms",
            "ForwardAgent",
            "CanonicalDomains",
            "VisualHostKey",
            "ExitOnForwardFailure",
            "EscapeChar",
            "GSSAPIDelegateCredentials",
            "IdentitiesOnly",
            "RekeyLimit",
            "TunnelDevice",
            "ControlMaster",
            "Ciphers",
            "KbdInteractiveAuthentication",
            "DynamicForward",
            "XAuthLocation",
            "SmartcardDevice",
            "ControlPath",
            "CanonicalizeHostname",
            "RequestTTY",
            "BindAddress",
            "StreamLocalBindUnlink",
            "StreamLocalBindMask",
            "RSAAuthentication",
            "RhostsRSAAuthentication",
            "ConnectionAttempts",
            "LocalForward",
            "PKCS11Provider",
            "PreferredAuthentications",
            "ServerAliveCountMax",
            "TCPKeepAlive",
            "Cipher",
            "local_tun",
            "Host",
            "ForwardX11Timeout",
            "Tunnel",
            "ChallengeResponseAuthentication",
            "GSSAPIKexAlgorithms",
            "HostbasedAuthentication",
            "CanonicalizeFallbackLocal",
            "Protocol",
            "ConnectTimeout",
            "ProxyJump",
            "SendEnv",
            "User",
            "GatewayPorts",
            "MACs",
            "Compression",
            "IPQoS",
            "GlobalKnownHostsFile",
            "ServerAliveInterval",
            "StrictHostKeyChecking",
            "KexAlgorithms",
            "CompressionLevel",
            "IdentityAgent",
            "ProxyUseFdpass",
            "GSSAPIAuthentication",
            "GSSAPIRenewalForcesRekey",
            "GSSAPITrustDns",
            "NoHostAuthenticationForLocalhost",
            "ProxyCommand",
            "PasswordAuthentication",
            "CanonicalizeMaxDots",
            "ControlPersist",
            "GSSAPIServerIdentity",
            "Match",
            "IdentityFile",
            "ForwardX11",
            "FingerprintHash",
        },
    )
)


def parse_ssh_man(ssh_man):
    flags_pattern = re.compile(r"ssh \[-(\w+)\]")
    options_pattern = re.compile(r"\[-(\w) (\S+)\]")

    flags = list(flags_pattern.search(ssh_man)[1])
    options = options_pattern.findall(ssh_man)

    return (flags, options)


def ssh_options(fn):
    flags, options = parse_ssh_man(SSH_MAN)
    for flag in flags:
        fn = click.option(f"-{flag}", flag, hidden=True, is_flag=True)(fn)
    for (option, name) in options:
        fn = click.option(
            f"-{option}", option, metavar=f"<{name}>", hidden=True, multiple=True
        )(fn)
    for opt in SSH_OPTS:
        fn = click.option(f"-o{opt}", opt, hidden=True, multiple=True)(fn)
    return fn


def normalize_token(token):
    if token.startswith("o") and len(token) > 1:
        return token.casefold()
    return token


def encode_options(kv):
    k, v = kv
    if k in SSH_OPTS:
        return {"o": [f"{k}={vv}" for vv in v]}
    else:
        return {k: v}


def use_interactive_ssm(is_a_tty: bool, command: Sequence[str], args: Dict) -> bool:
    if command:
        return False
    traditional_ssh_flags = ["D", "L", "N", "R", "T", "W", "w", "X", "Y"]
    for flag in traditional_ssh_flags:
        # if one of these flags is set to a truthy value then we need to speak traditional SSH
        if flag in args and args[flag]:
            return False
    return is_a_tty


@sym.command(
    short_help="Start a SSH session",
    context_settings={
        "ignore_unknown_options": True,
        "token_normalize_func": normalize_token,
    },
)
@resource_argument
@click.option("-p", "--port", default=22, type=int, show_default=True)
@click.option("--force-ssh/--no-force-ssh", default=False)
@click.argument("destination", required=False)
@click.argument("command", nargs=-1, required=False)
@ssh_options
@click.make_pass_decorator(GlobalOptions)
@command_require_bins("aws", "session-manager-plugin", "ssh")
@require_login
@loses_interactivity
def ssh(
    options: GlobalOptions,
    resource: str,
    destination: Optional[str],
    force_ssh: bool,
    port: int,
    command: Sequence[str],
    **kwargs,
) -> None:
    """
    Run SSH into an instance within a Sym resource group, by host, IP or instance ID. Examples of usage:

    \b
    sym ssh prod i-abcdefgh1234
    sym ssh staging 10.20.30.40
    SYM_RESOURCE=staging sym ssh 10.20.30.40

    Standard SSH options can be supplied to the command like this:

    \b
    sym ssh test 10.20.30.40 -o ControlMaster=yes -o ControlPath=~/.tmp/cp -o ControlPersist=10s -v

    """
    ssh_args = keywords_to_options(map(encode_options, kwargs.items()))
    if not destination:
        """
        Ansible will use SSH commands with no destination to audit the local SSH capabilities. When
        we detect this is happening, pass the arguments through as-is.
        """
        raw_ssh({"p": str(port)}, *ssh_args)
        return

    client = SAMLClientFactory.create_saml_client(resource, options)
    client.send_analytics_event()

    client.dprint(f"ssh: args={ssh_args}")
    instance = get_ec2_client(client).load_instance_by_alias(destination)
    new_client = SAMLClientFactory.clone(client, aws_region=instance.region)

    interactive_ssm = (
        use_interactive_ssm(
            is_a_tty=sys.stdin.isatty(),
            command=command,
            args=kwargs,
        )
        and not force_ssh
    )

    if interactive_ssm:
        start_interactive_command(new_client, instance.instance_id, command=command)
    else:
        start_ssh_session(
            new_client,
            instance.instance_id,
            port,
            args=ssh_args,
            command=command,
            wrap=False,
        )
