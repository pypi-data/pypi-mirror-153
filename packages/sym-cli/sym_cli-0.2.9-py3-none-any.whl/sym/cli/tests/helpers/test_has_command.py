from sym.shared.cli.helpers.os import has_command

from sym.cli.tests.helpers.sandbox import Sandbox


def test_has_command_not_found(sandbox: Sandbox) -> None:
    with sandbox.push_exec_path():
        assert not has_command("foo")


def test_has_command_found(sandbox: Sandbox) -> None:
    sandbox.create_file("bin/foo", 0o755)
    with sandbox.push_exec_path():
        assert has_command("foo")


def test_has_command_not_executable(sandbox: Sandbox) -> None:
    sandbox.create_file("bin/foo", 0o644)
    with sandbox.push_exec_path():
        assert not has_command("foo")
