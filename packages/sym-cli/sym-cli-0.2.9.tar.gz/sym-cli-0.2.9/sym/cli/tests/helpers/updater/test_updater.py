import datetime
import os
import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from semver import VersionInfo
from sym.shared.cli.helpers.updater import FAIL_LOG_PATH

from sym.cli.helpers.config import Config, SymConfigFile

V1 = VersionInfo.parse("0.0.1")


def test_pipx_path(pipx_updater):
    assert pipx_updater.is_pipx() == True


def test_sitepackage_path(sitepackage_updater):
    assert sitepackage_updater.is_sitepackage() == True


def test_brew_path(brew_updater):
    assert brew_updater.is_brew() == True


def test_local_if_v0(updater):
    updater.dir = Path("/foo/bar")
    assert updater.is_local() == True
    updater.get_current_version = MagicMock(return_value=V1)
    assert updater.is_local() == False


def test_default_path(updater):
    assert (updater.dir / "sym" / "cli").exists() == True


def test_noop_if_local(updater):
    assert updater.is_local() == True
    assert updater.should_check() == False


def test_no_manual_if_local(updater):
    updater.update = MagicMock()
    updater.manual_update()
    updater.update.assert_not_called()


def test_checks_first_time(pipx_updater):
    assert pipx_updater.should_check() == True


def test_checks_first_time_no_autoupdate(pipx_updater):
    Config.instance()["autoupdate"] = "false"
    assert pipx_updater.should_check() == False


def test_no_check_second_time(pipx_updater):
    assert pipx_updater.should_check() == True
    assert pipx_updater.should_check() == False


def test_check_after_a_day(pipx_updater, time_travel):
    assert pipx_updater.should_check() == True
    time_travel.tick(delta=datetime.timedelta(days=1))
    assert pipx_updater.should_check() == True


def test_get_version(updater):
    assert updater.get_latest_version() is not None
    assert updater.get_latest_version().major == 0
    assert updater.get_latest_version().minor >= 2


def test_needs_update(pipx_updater):
    pipx_updater.get_current_version = MagicMock(return_value=V1)
    assert pipx_updater.needs_update() is True


def test_needs_no_update(pipx_updater):
    pipx_updater.get_current_version = MagicMock(return_value=V1)
    pipx_updater.get_latest_version = MagicMock(return_value=V1)
    assert pipx_updater.needs_update() is False


def test_failed_fetch(pipx_updater):
    pipx_updater.get_latest_version = MagicMock(return_value=None)
    assert pipx_updater.needs_update() is False


def test_update_sitepackage(sitepackage_updater, capture_command):
    with capture_command():
        assert sitepackage_updater._update() == True
    capture_command.assert_command(re.compile(r"pip install -U sym-cli"))


def test_update_sitepackage_failed(sitepackage_updater, capture_command):
    capture_command.register_output("pip", "", exit_code=1)
    with capture_command():
        assert sitepackage_updater._update() == False


def test_update_pipx(pipx_updater, capture_command):
    with capture_command():
        assert pipx_updater._update() == True
    capture_command.assert_command(["pipx", "upgrade", "sym-cli"])


def test_update_pipx_failed(pipx_updater, capture_command):
    capture_command.register_output("pipx", "", exit_code=1)
    with capture_command():
        assert pipx_updater._update() == False


def test_update_brew(brew_updater, capture_command):
    capture_command.register_output(r"brew --repo", "/foo/bar")
    with capture_command():
        brew_updater.latest_version = V1
        assert brew_updater._update() == True
    capture_command.assert_command(
        ["brew", "--repo", "symopsio/tap"],
        ["git", "pull", "origin", "master"],
        ["brew", "install", "sym@0.0.1"],
        ["brew", "link", "sym@0.0.1"],
    )


def test_update_brew_failed(brew_updater, capture_command):
    capture_command.register_output("brew", "", exit_code=1)
    with capture_command():
        assert brew_updater._update() == False


def test_update_brew_failed_debug(brew_updater, capture_command, capsys):
    capture_command.register_output("brew", "an error!", exit_code=1)
    with capture_command():
        brew_updater.debug = True
        assert brew_updater._update() == False
        assert "an error!" in capsys.readouterr().err


def test_update_brew_timeout(brew_updater, capture_command, capsys):
    capture_command.register_output(r"brew --repo", "/foo/bar")
    capture_command.register_output(r"brew install", "something slow...", timeout=True)
    with capture_command():
        brew_updater.latest_version = V1
        brew_updater.debug = True
        assert brew_updater._update() == False

    capture_command.assert_command(
        ["brew", "--repo", "symopsio/tap"],
        ["git", "pull", "origin", "master"],
        ["brew", "install", "sym@0.0.1"],
        ["brew", "link", "sym"],
    )

    config_file = SymConfigFile(file_name=FAIL_LOG_PATH, uid_scope=False)
    assert str(config_file.path) in capsys.readouterr().err
    assert "something slow..." in config_file.read()


@pytest.mark.skipif(not os.getenv("CI"), reason="skipping real requests locally")
def test_update_other(other_updater):
    version = other_updater.get_latest_version()
    assert other_updater._update() == True
    assert (other_updater.dir / "sym").exists() == True
    assert str(version) in (other_updater.dir / "sym" / "cli" / "version.py").read_text()
