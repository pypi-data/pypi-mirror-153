import pytest
from sym.shared.cli.tests.helpers.capture import CaptureCommand

from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = pytest.mark.usefixtures("click_context")


@pytest.mark.parametrize(argnames=["constructor"], argvalues=[[AwsProfile]])
def test_aws_profile(
    test_context_with_creds: TestContextFixture[AwsProfile],
    capture_command: CaptureCommand,
) -> None:
    with test_context_with_creds(debug=False) as aws_profile:
        with capture_command():
            aws_profile.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command("aws ssm start-session --target i-0123456789abcdef")


@pytest.mark.parametrize(argnames=["constructor"], argvalues=[[AwsProfile]])
def test_aws_profile_debug(
    test_context_with_creds: TestContextFixture[AwsProfile],
    capture_command: CaptureCommand,
) -> None:
    with test_context_with_creds(debug=True) as aws_profile:
        with capture_command():
            aws_profile.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command("aws ssm start-session --target i-0123456789abcdef")
