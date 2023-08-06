import click

from sym.cli.decorators import require_login
from sym.cli.helpers.config import Config
from sym.cli.helpers.params import get_profiles

from .sym import sym


@sym.command(short_help="List available resource groups")
@click.option(
    "--format",
    required=True,
    type=click.Choice(["full", "simple"]),
    default="full",
)
@require_login
def resources(format) -> None:
    """List resource available to access with Sym.

    In simple mode, this is just a newline-delimited list.
    In full mode (default), the default resource is marked with an asterisk (*), and aliases are specified.
    """
    default = Config.instance().get("default_resource")
    for (slug, profile) in get_profiles().items():
        if format == "simple":
            click.echo("\n".join([slug, *profile.aliases]))
        else:
            star = "* " if default == slug else ""
            aliases = f" [{', '.join(profile.aliases)}]" if profile.aliases else ""
            click.echo(f"{star}{slug}{aliases} ({profile.display_name})")
