import tempfile
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from typing import Callable, ContextManager, Iterator, Tuple, Type, TypeVar

import click
import pytest
from _pytest.monkeypatch import MonkeyPatch
from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.tests.helpers.capture import CaptureCommand

from sym.cli.helpers.config import Config
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.saml_clients import aws_profile
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.conftest import CustomOrgFixture
from sym.cli.tests.helpers.sandbox import Sandbox

P = TypeVar("P", bound=SAMLClient)
TestContextFixture = Callable[..., ContextManager[P]]


@pytest.fixture
def config_with_duplicate_sections() -> str:
    return dedent(
        """
        [custom]
        app_id  = xxx
        [custom]
        app_id  = abc
        username = u123
        """
    )


@pytest.fixture
def test_context(
    constructor: Type[P],
    sandbox: Sandbox,
    custom_org: CustomOrgFixture,
    capture_command: CaptureCommand,
    fake_creds_env_str: str,
) -> TestContextFixture[P]:
    @contextmanager
    def context(*, debug: bool) -> Iterator[P]:
        capture_command.register_output(r"env", fake_creds_env_str)
        with sandbox.push_xdg_config_home(), custom_org("launch-darkly"):
            sandbox.create_binary(f"bin/{constructor.binary}")
            with sandbox.push_exec_path():
                yield constructor("catamorphic", options=GlobalOptions(debug=debug))

    return context


@pytest.fixture
def test_context_with_creds(
    constructor: Type[P],
    sandbox: Sandbox,
    custom_org: CustomOrgFixture,
    monkeypatch: MonkeyPatch,
) -> TestContextFixture[P]:
    @contextmanager
    def context(*, debug: bool) -> Iterator[P]:
        path = sandbox.path / ".aws" / "credentials"
        creds = "\n".join(
            [
                "[catamorphic]",
                "aws_access_key_id=ASIA4GNNUMIHHBPSAQC3",
                "aws_secret_access_key=xxx",
                "aws_session_token=xxx",
            ]
        )
        monkeypatch.setattr(aws_profile, "get_identity", lambda x: {})
        with push_env("AWS_CREDENTIAL_FILE", str(path)):
            setattr(aws_profile, "AwsCredentialsPath", path)
            with sandbox.push_xdg_config_home(), custom_org("launch-darkly"):
                sandbox.create_binary(f"bin/{constructor.binary}")
                sandbox.create_file(".aws/credentials", 0o755, creds)
                with sandbox.push_exec_path():
                    yield constructor("catamorphic", options=GlobalOptions(debug=debug))

    return context


def _subprocess_friendly_asserter(args: Tuple[Type[P], Sandbox]) -> None:
    constructor, sandbox, expected_command = args
    monkeypatch = MonkeyPatch()
    capture_command = CaptureCommand(monkeypatch)

    monkeypatch.setattr(SAMLClient, "check_is_setup", lambda self: ...)

    with sandbox.push_xdg_config_home(), sandbox.push_exec_path(), capture_command():
        outputs = [
            "AWS_REGION=foobar\nAWS_FOOBAR=baz\nAWS_OKTA_SESSION_EXPIRATION=1600494616\n"
        ] * 2
        capture_command.enqueue_outputs(*outputs)
        Config.instance()["org"] = "sym"
        with click.Context(click_command) as ctx:
            ctx.ensure_object(GlobalOptions)
            constructor("test", options=GlobalOptions(debug=False)).exec("env")
            capture_command.assert_command(*expected_command)


@pytest.fixture
def subprocess_friendly_asserter(constructor: Type[P]):
    with tempfile.TemporaryDirectory() as tmpdirname:
        sandbox = Sandbox(Path(tmpdirname))
        sandbox.create_binary(f"bin/{constructor.binary}")
        yield (_subprocess_friendly_asserter, constructor, sandbox)
