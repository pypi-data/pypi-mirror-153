import json
import os
from contextlib import ExitStack
from pathlib import Path
from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest
import responses
from freezegun import freeze_time
from semver import VersionInfo
from sym.shared.cli.helpers.updater import SymUpdater

CURRENT_ISH_VERSION = VersionInfo.parse("0.2.7")


@pytest.fixture
def time_travel() -> Iterator:
    with patch("yaml.safe_dump"):  # YAML can't serialize FakeDatetimes
        with freeze_time() as time:
            yield time


@pytest.fixture
def pypi_response():
    def responder(name) -> dict:
        return json.load((Path(__file__).parent / "responses" / f"{name}.json").open())

    return responder


@pytest.fixture
def http_mock(pypi_response) -> Iterator:
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        if os.getenv("CI"):
            rsps.add_passthru("http")  # make real requests on CI
        else:
            rsps.add(
                responses.GET,
                "https://pypi.org/pypi/sym-cli/json",
                json=pypi_response("sym-cli"),
            )
            rsps.add(
                responses.GET,
                f"https://pypi.org/pypi/sym-cli/{CURRENT_ISH_VERSION}/json",
                json=pypi_response("sym-cli-0.2.7"),
            )
        yield rsps


@pytest.fixture
def updater(sandbox, http_mock) -> Iterator[SymUpdater]:
    with ExitStack() as stack:
        stack.enter_context(sandbox.push_home())
        stack.enter_context(sandbox.push_xdg_config_home())
        stack.enter_context(sandbox.push_exec_path())

        updater = MagicMock(wraps=SymUpdater)()
        updater._env_is_local = lambda: False
        yield updater


@pytest.fixture
def other_updater(sandbox, updater) -> SymUpdater:
    updater.dir = sandbox.create_dir("my-sym-cli")
    return updater


@pytest.fixture
def sitepackage_updater(sandbox, updater) -> SymUpdater:
    root = Path() / "foo"
    sandbox.create_binary(root / "bin" / "pip")
    updater.dir = sandbox.create_dir(root / "lib" / "python3.8" / "site-packages")
    return updater


@pytest.fixture
def pipx_updater(sandbox, updater) -> SymUpdater:
    sandbox.create_binary("bin/pipx")
    updater.is_local = MagicMock(return_value=False)
    updater.dir = (
        sandbox.path
        / "home"
        / ".local"
        / "pipx"
        / "venvs"
        / "sym-cli"
        / "lib"
        / "python3.8"
        / "site-packages"
    )
    return updater


@pytest.fixture
def brew_updater(sandbox, updater) -> SymUpdater:
    sandbox.create_binary("bin/brew")
    sandbox.create_binary("bin/git")
    updater.is_local = MagicMock(return_value=False)
    updater.dir = (
        Path("/")
        / "usr"
        / "local"
        / "Cellar"
        / "sym-cli"
        / "0.0.0"
        / "libexec"
        / "lib"
        / "python3.8"
        / "site-packages"
    )
    return updater
