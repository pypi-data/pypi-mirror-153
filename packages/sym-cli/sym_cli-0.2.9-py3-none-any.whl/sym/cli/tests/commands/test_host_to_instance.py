import pytest
from expects import *

TEST_HOST = "test-host"
TEST_INSTANCE = "test-instance"


def describe_instances_stub(make_stub):
    ec2 = make_stub("ec2")
    ec2.add_response(
        "describe_instances",
        {"Reservations": [{"Instances": [{"InstanceId": TEST_INSTANCE}]}]},
    )


@pytest.fixture
def host_to_instance_tester(command_tester):
    return command_tester(["host-to-instance", "test", TEST_HOST])


def test_host_to_instance(
    host_to_instance_tester,
):
    def setup(make_stub):
        describe_instances_stub(make_stub)

    with host_to_instance_tester(setup=setup) as result:
        expect(result.output.strip()).to(equal(TEST_INSTANCE))
