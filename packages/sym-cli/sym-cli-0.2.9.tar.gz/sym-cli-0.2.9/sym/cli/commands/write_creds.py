from typing import Optional

import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from sym.cli.actions.action_registry import ActionRegistry
from sym.cli.data.request_data import RequestData
from sym.cli.decorators import command_require_bins, loses_interactivity, require_login
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.options import resource_argument
from sym.cli.saml_clients.aws_profile import AwsCredentialsPath

from .sym import sym  # TODO: this should be an absolute import


@sym.command(short_help="Write out AWS credentials")
@resource_argument
@click.option(
    "--path",
    help="Write credentials to a specific file",
    default=str(AwsCredentialsPath),
    show_default=True,
    type=click.Path(exists=True, dir_okay=False, writable=True),
)
@optgroup.group(
    "Profile Name",
    cls=MutuallyExclusiveOptionGroup,
    help="Settings which change the profile that credentials are written to",
)
@optgroup.option(
    "--profile",
    help="Profile name",
)
@optgroup.option(
    "--prefix",
    help="Prefix for profile name",
    default="sym",
    show_default=True,
)
@click.make_pass_decorator(GlobalOptions)
@command_require_bins("aws", "session-manager-plugin")
@require_login
@loses_interactivity
def write_creds(
    options: GlobalOptions,
    resource: str,
    path: str,
    profile: Optional[str],
    prefix: str,
) -> None:
    """Write out approved credentials for the specified Sym RESOURCE to
    a profile in your AWS credentials file.

    \b
    Example:
        `sym write-creds test --profile my-test-profile --path path/to/credentials`
    """
    request_data = RequestData(
        action="write_creds",
        resource=resource,
        global_options=options,
        params={"path": path, "profile": profile, "prefix": prefix},
    )
    ActionRegistry.execute(request_data)
