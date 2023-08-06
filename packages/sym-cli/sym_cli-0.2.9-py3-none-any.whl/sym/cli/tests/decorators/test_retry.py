import pytest

from sym.cli.decorators import retry


class NewError(Exception):
    pass


def test_retries():
    count = 0

    @retry(NewError)
    def fn():
        nonlocal count

        count += 1
        if count == 1:
            raise NewError

    fn()
    assert count == 2


def test_ultimately_raises():
    @retry(NewError)
    def fn():
        raise NewError

    with pytest.raises(NewError):
        fn()
