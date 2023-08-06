from contextlib import contextmanager
from typing import List, Sequence

import pytest
from click.testing import Result as ClickTestResult
from expects import *
from sym.shared.cli.helpers.contexts import push_envs
from sym.shared.cli.tests.helpers.capture import CaptureCommand

from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.sandbox import Sandbox
from sym.cli.tests.matchers import fail_with, succeed


@pytest.fixture
def command_login_tester(click_setup):
    def tester(args, envs={}):
        with click_setup(set_org=False) as runner:
            with push_envs(envs):
                result = runner.invoke(click_command, args)
                assert result.exit_code > 0
                assert "Error: Please run `sym login` first" in result.output

    return tester


@pytest.fixture
def command_tester(
    click_context,
    click_setup,
    ssm_bins,
    env_creds,
    boto_stub,
    saml_client: SAMLClient,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def tester(command: Sequence[str], setup=None, **kwargs):
        stubs = []

        def make_stub(service):
            stub = boto_stub(service)
            stubs.append(stub)
            return stub

        if setup:
            setup()

        teardown_ = kwargs.get("teardown")

        @contextmanager
        def context(setup=None, teardown=None, exception=None):
            with click_setup() as runner:
                with click_context:
                    if setup:
                        setup(make_stub)

                with capture_command():
                    result = runner.invoke(
                        click_command, command, catch_exceptions=False, echo=True
                    )
                    if exception:
                        expect(result).to(fail_with(exception))
                    else:
                        expect(result).to(succeed())
                    yield result

                for stub in stubs:
                    stub.assert_no_pending_responses()

                if teardown:
                    teardown()
                if teardown_:
                    teardown_()

        return context

    return tester


@pytest.fixture
def simple_command_tester(wrapped_cli_runner):
    """Run the click CliRunner with a custom invoke method.

    Use this fixture rather than command_tester to allow other fixtures
    access to information about processes and functions inside the CliRunner
    isolated environment. For example, if you need to know what subprocesses
    were run, or what functions were called via patch.

    Example:
        # in this version, assert_called_once() will succeed
        # mock_execute_write_creds.call_count == 1
        with patch.object(CommandHandler, "execute_write_creds") as mock_execute_write_creds:
            result = simple_command_tester([
                "write-creds",
                "test",
                "--profile",
                "test-profile",
                "--path",
                 "test/path"
            ])
            mock_execute_write_creds.assert_called_once()

        # in this version, assert_called_once() will fail
        # mock_execute_write_creds.call_count == 0
        with patch.object(CommandHandler, "execute_write_creds") as mock_execute_write_creds:
            command_tester(["write-creds", "test", "--profile", "test-profile", "--path", "test/path"])
            mock_execute_write_creds.assert_called_once()
    """

    def f(
        click_args: List[str],
    ) -> ClickTestResult:
        """
        Args:
            echo: Allow prints from .invoke to be shown
        """

        return wrapped_cli_runner.invoke(
            click_command, click_args, catch_exceptions=False
        )

    return f
