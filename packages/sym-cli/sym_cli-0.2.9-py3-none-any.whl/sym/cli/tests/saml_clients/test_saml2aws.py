from multiprocessing import Pool

import pytest
from expects import *
from sym.shared.cli.tests.helpers.capture import CaptureCommand

from sym.cli.helpers.config import SymConfigFile
from sym.cli.saml_clients.saml2aws import Saml2Aws
from sym.cli.tests.helpers.sandbox import Sandbox
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = [
    pytest.mark.usefixtures("click_context"),
    pytest.mark.parametrize(argnames=["constructor"], argvalues=[[Saml2Aws]]),
]


def test_saml2aws(
    test_context: TestContextFixture[Saml2Aws], capture_command: CaptureCommand
) -> None:
    with test_context(debug=False) as saml2aws:
        with capture_command():
            saml2aws.exec("aws", "ssm", "start-session", target="i-0123456789abcdef")
    capture_command.assert_command(
        f"saml2aws --config {saml2aws.config_file} --idp-account sym-catamorphic --skip-prompt exec -- env",
        f"saml2aws --version",
        f"saml2aws --config {saml2aws.config_file} --idp-account sym-catamorphic --skip-prompt login",
        f"saml2aws --config {saml2aws.config_file} --idp-account sym-catamorphic --skip-prompt exec -- 'aws ssm start-session --target i-0123456789abcdef'",
    )


def test_saml2aws_is_setup(
    test_context: TestContextFixture[Saml2Aws],
    capture_command: CaptureCommand,
    sandbox: Sandbox,
    config_with_duplicate_sections: str,
) -> None:
    with sandbox.push_home():
        sandbox.create_file("home/.saml2aws", contents=config_with_duplicate_sections)
        with test_context(debug=False) as saml2aws:
            with capture_command():
                capture_command.register_output(
                    "saml2aws --version", "2.26.2", stderr=True
                )
                assert saml2aws.is_setup() is True


def test_saml2aws_get_creds(
    test_context: TestContextFixture[Saml2Aws],
    capture_command: CaptureCommand,
) -> None:
    with test_context(debug=False) as saml2aws:
        with capture_command():
            expect(saml2aws.get_creds()).to(have_keys({"AWS_REGION": "foobar"}))


def test_saml2aws_session_length(test_context: TestContextFixture[Saml2Aws]):
    with test_context(debug=False) as saml2aws:
        saml2aws.options.session_length = 60
        expect(
            dict(saml2aws.ensure_config()[saml2aws._section_name]),
        ).to(have_key("aws_session_duration", "3600"))


def test_saml2aws_debug(
    test_context: TestContextFixture[Saml2Aws], capture_command: CaptureCommand
) -> None:
    with test_context(debug=True) as saml2aws:
        with capture_command():
            saml2aws.exec("env")
    capture_command.assert_command(
        f"saml2aws --verbose --config {saml2aws.config_file} --idp-account sym-catamorphic --skip-prompt exec -- env",
        f"saml2aws --version",
        f"saml2aws --verbose --config {saml2aws.config_file} --idp-account sym-catamorphic --skip-prompt login",
        f"saml2aws --verbose --config {saml2aws.config_file} --idp-account sym-catamorphic --skip-prompt exec -- env",
    )


def test_saml2aws_multi_threads(subprocess_friendly_asserter) -> None:
    f, constructor, sandbox = subprocess_friendly_asserter
    with sandbox.push_xdg_config_home():
        config_file = SymConfigFile(resource="test", file_name="saml2aws.cfg")
    commands = (
        f"saml2aws --config {config_file} --idp-account sym-test --skip-prompt exec -- env",
        f"saml2aws --version",
        f"saml2aws --config {config_file} --idp-account sym-test --skip-prompt login",
        f"saml2aws --config {config_file} --idp-account sym-test --skip-prompt exec -- env",
    )
    with Pool(processes=4) as pool:
        pool.map(f, [(constructor, sandbox, commands)] * 100)
