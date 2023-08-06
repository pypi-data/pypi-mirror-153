from multiprocessing import Pool

from sym.cli.helpers.config import Config
from sym.cli.helpers.ssh import _preprocess_args, maybe_gen_ssh_key, ssh_key_and_config
from sym.cli.tests.conftest import click_command, empty_saml_client, setup_context
from sym.cli.tests.helpers.sandbox import Sandbox


def _gen_ssh_key_fn(_i=0):
    with setup_context(click_command):
        maybe_gen_ssh_key(empty_saml_client())


def test_gen_ssh_key(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        with Pool(processes=4) as pool:
            pool.map(_gen_ssh_key_fn, range(10))

        ssh_key, _ = ssh_key_and_config(empty_saml_client())
        with ssh_key as f:
            assert "PRIVATE KEY" in f.read()


def test_gen_ssh_key_exists(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        _gen_ssh_key_fn()
        ssh_key, _ = ssh_key_and_config(empty_saml_client())

        with ssh_key as f:
            key = f.read()

        with Pool(processes=4) as pool:
            pool.map(_gen_ssh_key_fn, range(10))

        with ssh_key as f:
            assert key == f.read()


def test_preprocess_args_invalid_controlpath_equals(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        processed = _preprocess_args(
            empty_saml_client(),
            "fake-instance",
            ["-o", "ControlPath=/path/to/fake/cp.socket", "-o", "ControlMaster=15m"],
        )
        assert processed == ["-o", "ControlMaster=no"]


def test_preprocess_args_invalid_controlpath_space(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        processed = _preprocess_args(
            empty_saml_client(),
            "fake-instance",
            ["-o", "ControlPath /path/to/fake/cp.socket", "-o", "ControlMaster     15m"],
        )
        assert processed == ["-o", "ControlMaster=no"]


def test_preprocess_args_valid_controlpath(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        Config.touch_instance("fake-instance")
        processed = _preprocess_args(
            empty_saml_client(),
            "fake-instance",
            ["-o", "ControlPath /path/to/fake/cp.socket", "-o", "ControlMaster 15m"],
        )
        assert processed == [
            "-o",
            "ControlPath /path/to/fake/cp.socket",
            "-o",
            "ControlMaster 15m",
        ]


def test_preprocess_args_after_ssh_error(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        Config.touch_instance("fake-instance", True)
        processed = _preprocess_args(
            empty_saml_client(),
            "fake-instance",
            ["-o", "ControlPath /path/to/fake/cp.socket", "-o", "ControlMaster 15m"],
        )
        assert processed == [
            "-o",
            "ControlMaster=no",
        ]
