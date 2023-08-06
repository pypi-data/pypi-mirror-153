from typing import Tuple

import click

from sym.cli.decorators import loses_interactivity, require_login
from sym.cli.helpers.global_options import GlobalOptions

from ..helpers.options import resource_argument
from .sym import sym


@sym.command("exec", short_help="Execute a command")
@resource_argument
@click.argument("command", nargs=-1)
@click.make_pass_decorator(GlobalOptions)
@require_login
@loses_interactivity
def sym_exec(options: GlobalOptions, resource: str, command: Tuple[str, ...]) -> None:
    """Use approved creds for RESOURCE to execute COMMAND."""
    from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

    saml_client = SAMLClientFactory.create_saml_client(resource, options)
    saml_client.log_subprocess_event(command)
    saml_client.exec(*command)
