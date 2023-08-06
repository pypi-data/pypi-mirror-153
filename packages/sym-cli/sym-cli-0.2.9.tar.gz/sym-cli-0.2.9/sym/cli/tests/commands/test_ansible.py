import os
import tempfile
from contextlib import ExitStack
from typing import Dict, List

import pytest
from sym.shared.cli.helpers.contexts import push_envs
from sym.shared.cli.tests.helpers.capture import CaptureCommand, c

from sym.cli.constants.env import (
    ANSIBLE_CONNECTION_PLUGINS,
    ANSIBLE_DEBUG,
    ANSIBLE_PIPELINING,
    ANSIBLE_SSH_ARGS,
    ANSIBLE_SSH_ARGS_DEBUG,
    ANSIBLE_SSH_ARGS_NO_CONTROL_MASTER,
    ANSIBLE_SSH_RETRIES,
    DEFAULT_ANSIBLE_SSH_ARGS,
    DEFAULT_ANSIBLE_SSH_RETRIES,
    ENABLED,
    OBJC_DISABLE_INITIALIZE_FORK_SAFETY,
    SYM_DEBUG,
    SYM_LOG_DIR,
    SYM_USE_CONTROL_MASTER,
    YES,
)
from sym.cli.helpers.ansible import ansible_connection_plugins_value
from sym.cli.helpers.params import get_ssh_user
from sym.cli.tests.helpers.sandbox import Sandbox

INVENTORY = "inventory.file"
PLAYBOOK = "playbook.file"
TEST_ACCOUNT = "foo-account"


_default_ansible_env = {
    ANSIBLE_SSH_RETRIES: DEFAULT_ANSIBLE_SSH_RETRIES,
    ANSIBLE_SSH_ARGS: DEFAULT_ANSIBLE_SSH_ARGS,
    ANSIBLE_PIPELINING: ENABLED,
}


DEFAULT_SSH_VERSION_OUTPUT = "OpenSSH_8.1p1, LibreSSL 2.7.3"
OLD_SSH_VERSION_OUTPUT = "OpenSSH_7.1p1, LibreSSL 2.7.3"


def get_caller_identity_stub(make_stub):
    sts = make_stub("sts")
    sts.add_response("get_caller_identity", {"Account": TEST_ACCOUNT})


def _common_ansible_setup(
    capture_command: CaptureCommand,
    sandbox: Sandbox,
    ssh_output: str = DEFAULT_SSH_VERSION_OUTPUT,
):
    capture_command.register_output(
        "ssh",
        ssh_output,
        stderr=True,
    )
    sandbox.create_binary("bin/ansible-playbook")


def _assert_ansible_subcommands(
    capture_command: CaptureCommand,
    ansible_env: Dict[str, str] = _default_ansible_env,
):
    capture_command.assert_commands(
        [
            c("ssh", "-V"),
            c("exec", "true"),
            c(
                "ansible-playbook",
                "-i",
                INVENTORY,
                PLAYBOOK,
                "--connection=ssh",
                f"--user={get_ssh_user()}",
                **ansible_env,
            ),
        ]
    )


def _ansible_playbook_tester(command_tester, extra_args: List[str] = []):
    exit_stack = ExitStack()
    temp_dir = exit_stack.enter_context(tempfile.TemporaryDirectory())

    def setup():
        exit_stack.enter_context(push_envs({SYM_LOG_DIR: temp_dir}))

    def teardown():
        exit_stack.close()

    return command_tester(
        command=[
            "ansible-playbook",
            "test",
            "-i",
            INVENTORY,
            PLAYBOOK,
            *extra_args,
        ],
        setup=setup,
        teardown=teardown,
    )


@pytest.fixture
def ansible_playbook_tester_ssh(command_tester):
    return _ansible_playbook_tester(command_tester, ["--no-send-command"])


@pytest.fixture
def ansible_playbook_tester_ssh_no_control_master(command_tester):
    return _ansible_playbook_tester(
        command_tester, ["--no-send-command", "--no-control-master"]
    )


@pytest.fixture
def ansible_playbook_tester_send_command(command_tester):
    # TODO: we shouldn't need to pass this flag to bypass the SSH check when send-command is set
    return _ansible_playbook_tester(command_tester, ["--no-control-master"])


@pytest.fixture
def ansible_playbook_tester_send_command_low_forks(command_tester):
    # TODO: we shouldn't need to pass this flag to bypass the SSH check when send-command is set
    return _ansible_playbook_tester(command_tester, ["--no-control-master", "--forks=5"])


def test_ansible_playbook_ssh(
    ansible_playbook_tester_ssh,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def setup(_make_stub):
        _common_ansible_setup(capture_command, sandbox)

    with ansible_playbook_tester_ssh(setup=setup):
        _assert_ansible_subcommands(capture_command)


def test_ansible_playbook_ssh_old_version(
    ansible_playbook_tester_ssh,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def setup(_make_stub):
        _common_ansible_setup(
            capture_command,
            sandbox,
            ssh_output=OLD_SSH_VERSION_OUTPUT,
        )

    with ansible_playbook_tester_ssh(setup=setup):
        ansible_env = {
            ANSIBLE_SSH_RETRIES: DEFAULT_ANSIBLE_SSH_RETRIES,
            ANSIBLE_SSH_ARGS: ANSIBLE_SSH_ARGS_NO_CONTROL_MASTER,
            ANSIBLE_PIPELINING: ENABLED,
        }
        _assert_ansible_subcommands(capture_command, ansible_env)


def test_ansible_playbook_ssh_debug(
    ansible_playbook_tester_ssh,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    exit_stack = ExitStack()

    def setup(_make_stub):
        _common_ansible_setup(capture_command, sandbox)
        exit_stack.enter_context(push_envs({SYM_DEBUG: ENABLED}))

    def teardown():
        exit_stack.close()

    with ansible_playbook_tester_ssh(setup=setup, teardown=teardown):
        ansible_env = {
            ANSIBLE_SSH_RETRIES: DEFAULT_ANSIBLE_SSH_RETRIES,
            ANSIBLE_SSH_ARGS: ANSIBLE_SSH_ARGS_DEBUG,
            ANSIBLE_DEBUG: ENABLED,
        }
        _assert_ansible_subcommands(capture_command, ansible_env)


def test_ansible_playbook_ssh_no_control_master_via_arg(
    ansible_playbook_tester_ssh_no_control_master,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def setup(_make_stub):
        _common_ansible_setup(capture_command, sandbox)

    with ansible_playbook_tester_ssh_no_control_master(setup=setup):
        ansible_env = {
            ANSIBLE_SSH_RETRIES: DEFAULT_ANSIBLE_SSH_RETRIES,
            ANSIBLE_SSH_ARGS: ANSIBLE_SSH_ARGS_NO_CONTROL_MASTER,
            ANSIBLE_PIPELINING: ENABLED,
        }
        # Since we're disabling control master with an arg, we skip the SSH check
        capture_command.assert_commands(
            [
                c("exec", "true"),
                c("ansible-playbook", "-i", INVENTORY, PLAYBOOK, **ansible_env),
            ]
        )


def test_ansible_playbook_ssh_no_control_master_via_env(
    ansible_playbook_tester_ssh,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    exit_stack = ExitStack()

    def setup(_make_stub):
        _common_ansible_setup(capture_command, sandbox)
        exit_stack.enter_context(push_envs({SYM_USE_CONTROL_MASTER: "false"}))

    def teardown():
        exit_stack.close()

    with ansible_playbook_tester_ssh(setup=setup, teardown=teardown):
        ansible_env = {
            ANSIBLE_SSH_RETRIES: DEFAULT_ANSIBLE_SSH_RETRIES,
            ANSIBLE_SSH_ARGS: ANSIBLE_SSH_ARGS_NO_CONTROL_MASTER,
            ANSIBLE_PIPELINING: ENABLED,
        }
        # Since we're disabling control master with an env var, we skip the SSH check
        capture_command.assert_commands(
            [
                c("exec", "true"),
                c("ansible-playbook", "-i", INVENTORY, PLAYBOOK, **ansible_env),
            ]
        )


def test_ansible_playbook_send_command(
    ansible_playbook_tester_send_command,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def setup(make_stub):
        get_caller_identity_stub(make_stub)
        sandbox.create_binary("bin/ansible-playbook")

    with ansible_playbook_tester_send_command(setup=setup):
        ansible_env = {
            ANSIBLE_PIPELINING: ENABLED,
            OBJC_DISABLE_INITIALIZE_FORK_SAFETY: YES,
            ANSIBLE_CONNECTION_PLUGINS: ansible_connection_plugins_value(),
        }
        ansible_args = [
            "--connection=sym_aws_ssm",
            "--forks=10",
            f"--user={get_ssh_user()}",
            f"--extra-vars=ansible_aws_ssm_bucket='sym-ansible-{TEST_ACCOUNT}' ansible_aws_ssm_host_cmd='sym --saml-client aws-profile --log-dir {os.environ['SYM_LOG_DIR']} host-to-instance sym-ansible-test $HOST --json' ansible_aws_ssm_region='us-east-1' ansible_aws_ssm_profile='sym-ansible-test' ansible_aws_ssm_timeout='120'",
        ]
        capture_command.assert_commands(
            [
                c("exec", "true"),
                c(
                    "ansible-playbook",
                    "-i",
                    INVENTORY,
                    PLAYBOOK,
                    *ansible_args,
                    **ansible_env,
                ),
            ]
        )


def test_ansible_playbook_send_command_low_forks(
    ansible_playbook_tester_send_command_low_forks,
    capture_command: CaptureCommand,
    sandbox: Sandbox,
):
    def setup(make_stub):
        get_caller_identity_stub(make_stub)
        sandbox.create_binary("bin/ansible-playbook")

    with ansible_playbook_tester_send_command_low_forks(setup=setup):
        ansible_env = {
            ANSIBLE_PIPELINING: ENABLED,
            OBJC_DISABLE_INITIALIZE_FORK_SAFETY: YES,
            ANSIBLE_CONNECTION_PLUGINS: ansible_connection_plugins_value(),
        }
        ansible_args = [
            "--connection=sym_aws_ssm",
            "--forks=5",
            f"--user={get_ssh_user()}",
            f"--extra-vars=ansible_aws_ssm_bucket='sym-ansible-{TEST_ACCOUNT}' ansible_aws_ssm_host_cmd='sym --saml-client aws-profile --log-dir {os.environ['SYM_LOG_DIR']} host-to-instance sym-ansible-test $HOST --json' ansible_aws_ssm_region='us-east-1' ansible_aws_ssm_profile='sym-ansible-test' ansible_aws_ssm_timeout='120'",
        ]
        capture_command.assert_commands(
            [
                c("exec", "true"),
                c(
                    "ansible-playbook",
                    "-i",
                    INVENTORY,
                    PLAYBOOK,
                    *ansible_args,
                    **ansible_env,
                ),
            ]
        )


def test_ansible_no_login(command_login_tester):
    command_login_tester(["ansible"])
    command_login_tester(["ansible", "test"])
    command_login_tester(["ansible"], {"SYM_RESOURCE": "test"})
    command_login_tester(["ansible"], {"ENVIRONMENT": "test"})


def test_ansible_playbook_no_login(command_login_tester):
    command_login_tester(["ansible-playbook"])
    command_login_tester(["ansible-playbook", "test"])
    command_login_tester(
        ["ansible-playbook", "test", "-i", "inventory.txt", "playbook.yml"]
    )
    command_login_tester(["ansible-playbook"], {"SYM_RESOURCE": "test"})
    command_login_tester(["ansible-playbook"], {"ENVIRONMENT": "test"})
    command_login_tester(
        ["ansible-playbook", "-i", "inventory.txt", "playbook.yml"],
        {"ENVIRONMENT": "test"},
    )
