from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Sequence

from sym.shared.cli.data.global_options_base import GlobalOptionsBase

from sym.cli.errors import CliError
from sym.cli.helpers.ec2.client import RunningInstance


@dataclass
class CheckContext:
    options: GlobalOptionsBase
    resource: str
    regions: Sequence[str] = field(default_factory=list)
    running_instances: Sequence[RunningInstance] = field(default_factory=list)


class CheckError(CliError):
    def __init__(self) -> None:
        super().__init__(f"Checks failed!")


@dataclass
class CheckResult:
    error: Optional[Exception] = None
    success: bool = False
    msg: str = ""


class SymCheck(ABC):
    @abstractmethod
    def check(self, ctx: CheckContext) -> CheckResult:
        raise NotImplementedError()


def success(msg: str) -> CheckResult:
    result = CheckResult()
    result.success = True
    result.msg = msg
    return result


def failure(msg: str) -> CheckResult:
    result = CheckResult()
    result.msg = msg
    return result
