from json import dumps

import click

from sym.cli.decorators import loses_interactivity, require_login, skip_analytics
from sym.cli.helpers.ec2.factory import get_ec2_client
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.options import resource_argument
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory

from .sym import sym


@sym.command(short_help="Get an Instance ID for a host")
@click.option("--json", is_flag=True, hidden=True)
@resource_argument
@click.argument("host")
@click.make_pass_decorator(GlobalOptions)
@skip_analytics
@require_login
@loses_interactivity
def host_to_instance(
    options: GlobalOptions,
    resource: str,
    host: str,
    json: bool,
) -> None:
    """Get the Instance ID of a HOST associated with a Sym RESOURCE."""
    client = SAMLClientFactory.create_saml_client(resource, options)
    instance = get_ec2_client(client).load_instance_by_alias(host)
    if json:
        click.echo(dumps({"instance": instance.instance_id, "region": instance.region}))
    else:
        click.echo(instance.instance_id)
