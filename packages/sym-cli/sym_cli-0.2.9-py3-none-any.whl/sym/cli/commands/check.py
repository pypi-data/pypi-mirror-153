from typing import List

import click

from sym.cli.decorators import loses_interactivity
from sym.cli.helpers.check.runner import must_run_all
from sym.cli.helpers.global_options import GlobalOptions

from .sym import sym


@sym.command(hidden=True, short_help="Runs a series of checks against a Sym resource")
@click.make_pass_decorator(GlobalOptions)
@click.argument("resource")
@click.option("--instance", help="Instance ID(s) to check", multiple=True, default=[])
@loses_interactivity
def check(options: GlobalOptions, resource: str, instance: List[str]):
    """Run a series of checks against a Sym RESOURCE."""
    must_run_all(options, resource, instance)
