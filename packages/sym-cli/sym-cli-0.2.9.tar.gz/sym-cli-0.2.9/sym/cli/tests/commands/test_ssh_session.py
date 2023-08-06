import pytest
from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.tests.helpers.capture import CaptureCommand

from sym.cli.errors import SuppressedError
from sym.cli.helpers.config import Config
from sym.cli.tests.helpers.ec2.conftest import TEST_REGION

INSTANCE_ID = "123"
SESSION_ID = "456"


def update_config():
    Config.record_instance(INSTANCE_ID, region=TEST_REGION, alias="10.20.30.40")


def start_session_stub(make_stub):
    ssm = make_stub("ssm")
    ssm.add_response("start_session", {"SessionId": SESSION_ID})
    ssm.add_response(
        "terminate_session", {"SessionId": SESSION_ID}, {"SessionId": SESSION_ID}
    )


@pytest.fixture
def ssh_session_tester(command_tester):
    with push_env("SYM_SKIP_ENSURE_KEY", "1"):
        yield command_tester(["ssh-session", "test", "--instance", INSTANCE_ID])


def test_ssh_session(ssh_session_tester, capture_command: CaptureCommand):
    def setup(make_stub):
        update_config()
        start_session_stub(make_stub)

    with ssh_session_tester(setup=setup):
        capture_command.assert_command(
            ["exec", "true"],
            ["exec", "true"],
            ["session-manager-plugin"],
        )


def test_ssh_session_error(ssh_session_tester, capture_command: CaptureCommand):
    def setup(make_stub):
        update_config()
        start_session_stub(make_stub)
        capture_command.register_output(r"session-manager-plugin", "timeout", exit_code=1)

    with ssh_session_tester(setup=setup, exception=SuppressedError):
        capture_command.assert_command(
            ["exec", "true"],
            ["exec", "true"],
            ["session-manager-plugin"],
        )
