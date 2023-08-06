from textwrap import dedent
from typing import Sequence

import click

from sym.cli.decorators import command_require_bins, loses_interactivity, require_login
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.options import resource_argument
from sym.cli.helpers.ssh import get_ssh_user, start_ssh_tunnel
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from .sym import sym


def ssh_tunnel_help():
    try:
        ssh_user = get_ssh_user()
    except KeyError:
        ssh_user = "ubuntu"

    HELP = dedent(
        f"""
        Run a command that requires SSH connectivity (such as `scp`) with a Sym SSH Tunnel.

        sym ssh-tunnel RESOURCE PROGRAM OPTIONS

        Note that you must manually specify both the destination instance
        and your SSH user (usually {ssh_user}) in the OPTIONS.

        For example, to use `scp` to copy a remote file to your machine:

        \b
        sym ssh-tunnel prod scp {ssh_user}@i-0647ba4f8187ac121:~/file.txt file.txt

        If this command fails, try to first `sym ssh` into the instance, then try again.

        https://docs.symops.com/docs/ssh-tunnel
    """
    )


@sym.command(short_help="Run a command with a Sym SSH Tunnel", help=ssh_tunnel_help())
@resource_argument
@click.argument("program")
@click.argument("opts", nargs=-1, required=False)
@click.make_pass_decorator(GlobalOptions)
@command_require_bins("aws", "session-manager-plugin", "ssh")
@require_login
@loses_interactivity
def ssh_tunnel(
    options: GlobalOptions,
    resource: str,
    program: str,
    opts: Sequence[str],
) -> None:
    client = SAMLClientFactory.create_saml_client(resource, options)
    client.send_analytics_event()

    start_ssh_tunnel(client, program, opts)
