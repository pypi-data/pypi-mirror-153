from typing import Callable, Union

import click
from click_option_group import MutuallyExclusiveOptionGroup
from sym.shared.cli.helpers.envvar_option import EnvvarGroupedOption, EnvvarOption
from sym.shared.cli.helpers.util import flow

from sym.cli.constants.env import SYM_USE_CONTROL_MASTER
from sym.cli.errors import CliError
from sym.cli.helpers.config import Config
from sym.cli.helpers.params import get_resource_env_vars
from sym.cli.helpers.ssh import check_ssh_version


def config_option(
    name: str, help: str, default: Union[None, Callable[[], None]] = None, **kwargs
):
    def decorator(f):
        option_decorator = click.option(
            f"--{name}",
            help=help,
            prompt=True,
            default=default or (lambda: Config.instance().get(name)),
            **kwargs,
        )
        return option_decorator(f)

    return decorator


def _resource_arg_callback(ctx, param, resource: str):
    """
    The resource *arg* callback raises an exception when the user isn't logged in,
    or when the supplied resource isn't valid for the logged in user.
    Otherwise, it returns the resource.
    """
    if not Config.is_logged_in():
        raise CliError("Please run `sym login` first")
    if resource is None:
        # We do some really complicated stuff in SymGroup to automagically update args so that
        # "resource" doesn't need to follow the strict rules of being a positional arg.
        # For "ansible-playbook" and "ssh" commands, this can result in this callback getting invoked
        # twice, once with "None" value here.
        return None
    if not resource:
        raise click.BadParameter("Missing a resource!")
    return resource


def resource_option(f):
    """
    Used by the root command only. Subcommands that require a positional resource argument
    can get confused when the resource is provided via env var and is followed with arbitrary
    other args, so we have a special decorator in SymGroup copy the option into the
    right position. We don't use a callback or perform any special validation here,
    that validation will be performed when a subcommand uses the
    resource_argument decorator.
    """
    option_decorator = click.option(
        "--resource",
        help="The Sym resource to use",
        envvar=get_resource_env_vars(),
        default=lambda: Config.get_default("resource"),
        cls=EnvvarOption,
    )
    return option_decorator(f)


def resource_argument(f):
    option_decorator = click.argument(
        "resource",
        callback=_resource_arg_callback,
        envvar=get_resource_env_vars(),
        # We set required=False to ensure that the callback is always invoked. In the case where a
        # custom env var is used to specify the resource, but the user is not logged in, the callback
        # will correctly return a login error, rather than a missing argument error.
        required=False,
    )
    return option_decorator(f)


def ansible_options(f):
    group = MutuallyExclusiveOptionGroup("Ansible Roles")
    options = [
        group.option(
            "--ansible-aws-profile",
            help="The local AWS Profile to use for Ansible commands",
            envvar="AWS_PROFILE",
            cls=EnvvarGroupedOption,
        ),
        group.option(
            "--ansible-sym-resource",
            help="The Sym resource to use for Ansible commands",
            envvar="SYM_ANSIBLE_RESOURCE",
            callback=_resource_arg_callback,
            cls=EnvvarGroupedOption,
        ),
        click.option(
            "--control-master/--no-control-master",
            help="Allow SSH ControlPath caching",
            envvar=SYM_USE_CONTROL_MASTER,
            is_flag=True,
            default=check_ssh_version,
            cls=EnvvarOption,
        ),
        click.option(
            "--send-command/--no-send-command",
            help="Use SSM SendCommand instead of SSH",
            envvar="SYM_SEND_COMMAND",
            is_flag=True,
            default=True,
            cls=EnvvarOption,
            show_default=True,
        ),
        click.option(
            "--forks",
            help="Number of parallel subprocesses for ansible",
            default=10,
            show_default=True,
        ),
        click.option(
            "--command-timeout",
            help="The timeout for any given command",
            envvar="SYM_COMMAND_TIMEOUT",
            default=120,
            show_default=True,
        ),
    ]
    return flow(options, f)


def required_option(*args, if_, **kwargs):
    def _callback(ctx, param: str, value: str):
        if not value and if_(ctx):
            raise click.exceptions.UsageError(f"{param} is required")
        return value

    def wrapper(f):
        return click.option(*args, callback=_callback, **kwargs)(f)

    return wrapper
