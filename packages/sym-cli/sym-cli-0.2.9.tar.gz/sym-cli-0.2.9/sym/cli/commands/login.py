import click

from sym.cli.helpers.params import set_login_fields

from ..helpers.options import config_option
from ..helpers.org import infer_org_from_email
from .sym import sym


@sym.command(short_help="Log in to your sym account")
@config_option(
    "email",
    help="The email you use to log into your identity provider (e.g. Okta or GSuite).",
)
@config_option(
    "org",
    help="Your organizations's slug. Contact support if you need this.",
    default=lambda: infer_org_from_email(click.get_current_context().params["email"]),
)
def login(**kwargs) -> None:
    """Link your Sym account."""
    set_login_fields(**kwargs)
    click.echo("Sym successfully initalized!")
