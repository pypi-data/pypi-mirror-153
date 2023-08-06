from abc import ABC, abstractmethod
from typing import List

from sym.cli.data.request_data import RequestData
from sym.cli.errors import CliError
from sym.cli.helpers.check.model import SymCheck


class SymAction(ABC):
    def __init__(self, name):
        self.name = name

    def validate_inputs(self, request_data: RequestData) -> None:
        """Entry point to validate request data.

        Args:
            request_data: Operational request to validate before execution

        Raises:
            ValueError: if any part of request data is invalid (e.g. missing resource)
        """

    def get_requirements(self) -> List[SymCheck]:
        return []

    def invoke_requirements(self):
        requirements = self.get_requirements()
        failures = []
        failure_string = ""
        if requirements:
            for requirement in requirements:
                result = requirement.check(None)
                if not result.success:
                    failures.append(result)
                    failure_string = (
                        failure_string + f"Validation Error, message:{result.msg}\n"
                    )

        if len(failures) > 0:
            raise CliError(failures)

    @abstractmethod
    def execute(self, request_data: RequestData):
        pass
