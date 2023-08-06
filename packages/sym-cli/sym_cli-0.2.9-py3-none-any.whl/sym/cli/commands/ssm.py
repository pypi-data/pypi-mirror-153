import click

from sym.cli.decorators import command_require_bins, loses_interactivity, require_login
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from ..helpers.options import resource_argument
from .sym import sym


@sym.command(hidden=True, short_help="New SSM Session")
@resource_argument
@click.option(
    "--target", help="target instance id", metavar="<instance-id>", required=True
)
@click.make_pass_decorator(GlobalOptions)
@command_require_bins("aws", "session-manager-plugin")
@require_login
@loses_interactivity
def ssm(options: GlobalOptions, resource: str, target: str) -> None:
    """Use approved creds for RESOURCE to start an SSM session to an EC2 instance"""
    client = SAMLClientFactory.create_saml_client(resource, options)
    client.exec("aws", "ssm", "start-session", target=target)
