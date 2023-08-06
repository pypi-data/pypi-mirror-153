from multiprocessing import Pool

import pytest
from expects import expect, have_key
from sym.shared.cli.tests.helpers.capture import CaptureCommand

from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = [
    pytest.mark.usefixtures("click_context"),
    pytest.mark.parametrize(argnames=["constructor"], argvalues=[[AwsOkta]]),
]


def test_aws_okta(
    test_context: TestContextFixture[AwsOkta], capture_command: CaptureCommand
) -> None:
    with test_context(debug=False) as aws_okta:
        with capture_command():
            aws_okta.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command(
        "aws-okta exec sym-catamorphic -- env",
        "aws-okta --debug exec sym-catamorphic -- false",
        "aws-okta exec sym-catamorphic -- true",
        "aws-okta exec sym-catamorphic -- aws ssm start-session --target i-0123456789abcdef",
    )


def test_aws_okta_debug(
    test_context: TestContextFixture[AwsOkta], capture_command: CaptureCommand
) -> None:
    with test_context(debug=True) as aws_okta:
        with capture_command():
            aws_okta.exec("env")
    capture_command.assert_command(
        "aws-okta --debug exec sym-catamorphic -- env",
        "aws-okta --debug exec sym-catamorphic -- false",
        "aws-okta --debug exec sym-catamorphic -- true",
        "aws-okta --debug exec sym-catamorphic -- env",
    )


def test_aws_okta_session_length(test_context: TestContextFixture[AwsOkta]):
    with test_context(debug=False) as aws_okta:
        aws_okta.options.session_length = 60
        expect(
            dict(aws_okta.ensure_config()[f"profile {aws_okta._section_name}"]),
        ).to(have_key("session_ttl", "60m"))


def test_aws_okta_multi_threads(subprocess_friendly_asserter) -> None:
    commands = (
        "aws-okta exec sym-test -- env",
        "aws-okta --debug exec sym-test -- false",
        "aws-okta exec sym-test -- true",
        "aws-okta exec sym-test -- env",
    )
    f, *args = subprocess_friendly_asserter
    with Pool(processes=4) as pool:
        pool.map(f, [(*args, commands)] * 100)
