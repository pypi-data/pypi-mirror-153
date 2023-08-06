import re
from subprocess import CalledProcessError

import pytest

from sym.cli.decorators import intercept_errors
from sym.cli.errors import CliError


class NewError(Exception):
    pass


@intercept_errors({re.compile("already"): NewError}, quiet=True)
def _raise_error(message: str) -> None:
    raise CalledProcessError(returncode=1, cmd=(), stderr=message)


def test_intercept_error_match(click_context) -> None:
    with pytest.raises(NewError):
        _raise_error("File already exists.")


def test_intercept_error_non_match(click_context) -> None:
    with pytest.raises(CliError):
        _raise_error("File not found.")
