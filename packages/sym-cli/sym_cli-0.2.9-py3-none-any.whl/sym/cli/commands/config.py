from collections import defaultdict

import click
import immutables

from sym.cli.helpers.config import Config, ConfigSchema
from sym.cli.helpers.validations import validate_bool_str, validate_resource

from .sym import sym

NO_VALIDATION = lambda _: True
VALIDATIONS = defaultdict(
    lambda: NO_VALIDATION,
    {
        "default_resource": validate_resource,
        "autoupdate": validate_bool_str,
        "analytics": validate_bool_str,
    },
)


def key_callback(ctx, key: str):
    if key not in ConfigSchema.__annotations__:
        raise click.BadParameter(f"Unrecognized configuration key `{key}`")
    return key


def value_callback(ctx, value: str):
    if value is None:
        return None
    if not VALIDATIONS[ctx.params["key"]](value):
        raise click.BadParameter(f"Invalid value `{value}` for key `{ctx.params['key']}`")
    return value


def pformat(value, indent=0):
    if isinstance(value, (dict, immutables.Map)):
        lines = []
        for k, v in value.items():
            tabs = "\t" * indent
            lines.append(f"\n{tabs}{k}: {pformat(v, indent=indent+1)}")
        return "\n".join(lines)
    else:
        return value


@sym.command(hidden=True, short_help="get a config value")
@click.argument("key", callback=key_callback)
@click.argument("value", callback=value_callback, required=False)
def config(key: str, value: str) -> None:
    """Get a Sym config value."""
    if value is None:
        click.echo(pformat(Config.instance().get(key)))
    else:
        Config.instance()[key] = value


@sym.command(hidden=True, name="config:set", short_help="set a config value")
@click.argument("key", callback=key_callback)
@click.argument("value", callback=value_callback)
def config_set(key: str, value: str) -> None:
    """Set a Sym config value."""
    Config.instance()[key] = value


@sym.command(hidden=True, name="config:unset", short_help="unset a config value")
@click.argument("key", callback=key_callback)
def config_unset(key: str) -> None:
    """Unset a Sym config value."""
    Config.instance()[key] = None
