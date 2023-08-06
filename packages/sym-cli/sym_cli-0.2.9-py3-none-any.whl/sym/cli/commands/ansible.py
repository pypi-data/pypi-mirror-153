from typing import Optional, Tuple

import click

from sym.cli.actions.action_registry import ActionRegistry
from sym.cli.data.ansible_options import AnsibleOptions
from sym.cli.data.request_data import RequestData
from sym.cli.decorators import command_require_bins, loses_interactivity, require_login
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.options import ansible_options as click_ansible_options
from sym.cli.helpers.options import resource_argument

from .sym import sym


@sym.command(
    short_help="Run an Ansible command",
    context_settings={"ignore_unknown_options": True},
)
@resource_argument
@click.argument("command", nargs=-1)
@click_ansible_options
@click.make_pass_decorator(GlobalOptions)
@command_require_bins("ansible", "aws", "session-manager-plugin")
@require_login
@loses_interactivity
def ansible(
    options: GlobalOptions,
    resource: str,
    command: Tuple[str, ...],
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
    control_master: bool,
    send_command: bool,
    forks: int,
    command_timeout: int,
) -> None:
    """Run Ansible commands against an inventory of EC2 instances, using
    approved credentials from the Sym RESOURCE group.

    For a list of available Sym RESOURCES, run `sym resources`.

    \b
    Example:
        `sym ansible RESOURCE all -m ping`
    """

    ansible_options = AnsibleOptions(
        command=command,
        control_master=control_master,
        send_command=send_command,
        forks=forks,
        ansible_aws_profile=ansible_aws_profile,
        ansible_sym_resource=ansible_sym_resource,
        ssm_timeout=command_timeout,
    )

    request_data = RequestData(
        action="ansible",
        resource=resource,
        global_options=options,
        ansible_options=ansible_options,
    )

    ActionRegistry.execute(request_data)
