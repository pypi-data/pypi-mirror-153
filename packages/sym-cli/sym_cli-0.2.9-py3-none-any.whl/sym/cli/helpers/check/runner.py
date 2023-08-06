from typing import List

from sym.shared.cli.data.global_options_base import GlobalOptionsBase

from sym.cli.helpers.check.model import CheckContext, CheckError, SymCheck
from sym.cli.helpers.check.ssh import (
    EnsureSshKeyAuthorizedCheck,
    GenSshConfigCheck,
    GenSshKeyCheck,
)

from .core import DependenciesCheck, LoginCheck, ResourceCheck
from .ec2 import CallerIdentityCheck, DescribeInstanceCheck, DescribeRegionsCheck


def run_check(check: SymCheck, ctx: CheckContext) -> bool:
    result = check.check(ctx)
    if result.success:
        print("\u2713", result.msg)
        return True
    else:
        print("\u2717", result.msg)
        if result.error:
            print(result.error)
        return False


def get_checks(instances: List[str]) -> List[SymCheck]:
    checks = [
        LoginCheck(),
        DependenciesCheck("aws"),
        DependenciesCheck("session-manager-plugin"),
        DependenciesCheck("ssh-keygen"),
        ResourceCheck(),
        CallerIdentityCheck(),
        DescribeRegionsCheck(),
        GenSshConfigCheck(),
        GenSshKeyCheck(),
    ]
    for instance in instances:
        checks.append(DescribeInstanceCheck(instance))
        checks.append(EnsureSshKeyAuthorizedCheck(instance))
    return checks


def must_run_all(options: GlobalOptionsBase, resource: str, instances: List[str]):
    """
    Runs all checks with the supplied args.
    Raises a CheckError on the first check failure, or returns normally if all checks succeed.
    """
    ctx = CheckContext(options=options, resource=resource)
    checks = get_checks(instances)
    for check in checks:
        if not run_check(check, ctx):
            raise CheckError()
