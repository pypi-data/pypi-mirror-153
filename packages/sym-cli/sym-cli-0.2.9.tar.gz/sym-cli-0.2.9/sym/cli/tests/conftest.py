from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager, Iterator

import boto3
import click
import pytest
from _pytest.monkeypatch import MonkeyPatch
from botocore.stub import Stubber
from sym.shared.cli.helpers.envvar_option import reset_used
from sym.shared.cli.tests.conftest import *  # noqa

from sym.cli.helpers import boto
from sym.cli.helpers.config import Config, init
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.sym_group import SymGroup
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.sandbox import Sandbox

CustomOrgFixture = Callable[[str], ContextManager[None]]


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def click_context(sandbox):
    with sandbox.push_xdg_config_home():
        Config.instance()["org"] = "sym"
        Config.instance()["email"] = "y@symops.io"
        sandbox.create_binary(f"bin/{AwsOkta.binary}")
        with sandbox.push_exec_path():
            with click.Context(click_command) as ctx:
                ctx.ensure_object(GlobalOptions)
                yield ctx


@pytest.fixture
def click_setup(sandbox: Sandbox, wrapped_cli_runner):
    @contextmanager
    def context(set_org=True, set_client=True):
        runner = wrapped_cli_runner
        with runner.isolated_filesystem():
            with sandbox.setup(set_org=set_org, set_client=set_client):
                yield runner
        reset_used()

    return context


@pytest.fixture
def no_click_setup(sandbox: Sandbox):
    """no_click_setup includes the same functionality as
    click_setup but without loading any Click configuration
    """

    @contextmanager
    def context(set_org=True, set_client=True):
        with sandbox.setup(set_org=set_org, set_client=set_client):
            yield
        reset_used()

    return context


@pytest.fixture(autouse=True)
def patch_is_setup(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(SAMLClient, "check_is_setup", lambda self: ...)


@pytest.fixture
def custom_org(monkeypatch: MonkeyPatch) -> CustomOrgFixture:
    @contextmanager
    def custom_org(org: str) -> Iterator[None]:
        with monkeypatch.context() as mp:
            mp.setattr(Config, "get_org", classmethod(lambda cls: org))
            yield

    return custom_org


@pytest.fixture
def saml_client(sandbox: Sandbox, monkeypatch: MonkeyPatch, creds_env):
    def get_creds(self):
        return dict(creds_env)

    monkeypatch.setattr(AwsOkta, "get_creds", get_creds)

    def profile_matches_caller_identity(self):
        return True

    monkeypatch.setattr(
        AwsOkta, "_profile_matches_caller_identity", profile_matches_caller_identity
    )

    sandbox.create_binary(f"bin/{AwsOkta.binary}")
    with sandbox.push_exec_path():
        return AwsOkta("test", options=GlobalOptions(debug=False))


@pytest.fixture
def ssm_bins(sandbox: Sandbox):
    for binary in ["aws", "session-manager-plugin", "ssh"]:
        sandbox.create_binary(f"bin/{binary}")


@pytest.fixture
def boto_stub(monkeypatch: MonkeyPatch):
    stubs = {}

    def boto_client(_saml_client, service):
        if service in stubs:
            return stubs[service][0]

        client = boto3.client(service)
        stubber = Stubber(client)
        stubber.activate()

        stubs[service] = (client, stubber)
        return client

    monkeypatch.setattr(boto, "boto_client", boto_client)

    def get_stub(service):
        boto_client(None, service)
        return stubs[service][1]

    return get_stub


@contextmanager
def setup_context(click_command):
    with click.Context(click_command) as ctx:
        ctx.obj = GlobalOptions(saml_client_type=AwsProfile)
        yield


def empty_saml_client():
    return AwsProfile("test", options=GlobalOptions())


@pytest.fixture(autouse=True)
def cleanup(request):
    request.addfinalizer(SymGroup.reset_tees)


@pytest.fixture(autouse=True)
def init_cli():
    init("sym")
