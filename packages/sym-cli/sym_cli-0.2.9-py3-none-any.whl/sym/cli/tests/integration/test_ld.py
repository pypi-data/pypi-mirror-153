import json
import os
import subprocess
import tempfile

import pytest
from expects import *
from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.helpers.os import cd

LD_DIR = "./test/integration/docker-ansible-ld/sym"

pytestmark = pytest.mark.skipif(
    not os.getenv("SYM_INTEGRATION"),
    reason="skipping integration tests",
)


def run_login(config, run):
    run(
        "login",
        "--email",
        config.getoption("email"),
        "--org",
        config.getoption("org"),
    )


def test_ssh_old_instance(pytestconfig, integration_runner):
    with integration_runner() as run:
        run_login(pytestconfig, run)
        result = run(
            "--saml-client",
            "aws-profile",
            "ssh",
            pytestconfig.getoption("resource"),
            pytestconfig.getoption("instance"),
            "--",
            "uname",
            "-a",
        )
        expect(result.output).to(contain("Ubuntu"))


def test_ansible_playbook_old_instance(pytestconfig, integration_runner):
    with cd(LD_DIR), integration_runner() as run:
        run_login(pytestconfig, run)
        with open("inventory.txt", "w") as f:
            f.write(pytestconfig.getoption("instance") + "\n")
        with tempfile.TemporaryDirectory() as log_dir:
            result = run(
                "--saml-client",
                "aws-profile",
                "--log-dir",
                log_dir,
                "ansible-playbook",
                pytestconfig.getoption("resource"),
                "-i",
                "inventory.txt",
                "docker_test.yml",
                "-vvv",
            )
        expect(result.output).to(contain("ok=5"))


@pytest.mark.skip(reason="Need to automate spinning up more instances")
def test_ansible_playbook_new_instance(pytestconfig, integration_runner):
    with cd(LD_DIR), integration_runner() as run:
        run_login(pytestconfig, run)
        with push_env("DO_RUN", "true"):
            subprocess.run(["./bin/ld_reserve_instance"], check=True)
        with tempfile.TemporaryDirectory() as log_dir:
            result = run(
                "--log-dir",
                log_dir,
                "ansible-playbook",
                pytestconfig.getoption("resource"),
                "-i",
                "ec2.py",
                "docker_test.yml",
            )
        expect(result.output).to(contain("ok=5"))


def test_exec(pytestconfig, integration_runner):
    with cd(LD_DIR), integration_runner() as run:
        run_login(pytestconfig, run)
        result = run(
            "--saml-client",
            "aws-profile",
            "exec",
            pytestconfig.getoption("resource"),
            "--",
            "./ec2.py",
        )
        expect(json.loads(result.output)).to(have_keys("_meta", "ec2"))
