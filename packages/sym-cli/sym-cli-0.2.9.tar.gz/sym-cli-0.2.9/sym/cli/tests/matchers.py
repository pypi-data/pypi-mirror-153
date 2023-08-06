from click.testing import Result
from expects.matchers import Matcher


class succeed(Matcher):
    def _match(self, result: Result):
        if result.exit_code == 0:
            return True, ["command succeeded"]
        else:
            errors = [f"command had exit code {result.exit_code}"]
            if result.output:
                errors.append(f"command failed: {result.output}")
            return False, errors


class fail_with(Matcher):
    def __init__(self, exception_klass):
        self.exception_klass = exception_klass

    def _match(self, result: Result):
        if result.exit_code == 0:
            return False, ["command succeeded"]
        elif result.exit_code != self.exception_klass.exit_code:
            return False, [f"command failed with exit code {result.exit_code}"]
        else:
            return True, [
                f"command failed with exit code {self.exception_klass.exit_code}"
            ]
