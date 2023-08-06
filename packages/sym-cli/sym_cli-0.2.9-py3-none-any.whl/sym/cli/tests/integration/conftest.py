import os
import random
from contextlib import contextmanager

import boto3
import pytest
from expects import *

from sym.cli.sym import sym as click_command
from sym.cli.tests.matchers import succeed


def gen_instances():
    if not os.getenv("SYM_INTEGRATION"):
        yield "i-xxx"
        return

    ec2 = boto3.client("ec2")
    paginator = ec2.get_paginator("describe_instances")
    for response in paginator.paginate(
        Filters=[{"Name": "tag:CLITest", "Values": ["integration"]}]
    ):
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                yield instance["InstanceId"]


@pytest.fixture
def integration_runner(capfdbinary, sandbox, wrapped_cli_runner):
    @contextmanager
    def context():
        runner = wrapped_cli_runner
        with sandbox.push_xdg_config_home():

            def run(*args):
                result = runner.invoke(click_command, args, catch_exceptions=False)
                cap = capfdbinary.readouterr()
                result.stdout_bytes = cap.out
                result.stderr_bytes = cap.err

                expect(result).to(succeed())
                return result

            yield run

    return context


def pytest_addoption(parser):
    parser.addoption("--email", default="ci@symops.io")
    parser.addoption("--org", default="sym")
    parser.addoption("--instance", default=random.choice(list(gen_instances())))
    parser.addoption("--resource", default="test")
