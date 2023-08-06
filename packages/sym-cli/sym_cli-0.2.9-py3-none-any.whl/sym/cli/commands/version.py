import click

from ..version import __version__
from .sym import sym


@sym.command(short_help="Print the version")
def version() -> None:
    """Print the Sym CLI version."""
    click.echo(__version__)
