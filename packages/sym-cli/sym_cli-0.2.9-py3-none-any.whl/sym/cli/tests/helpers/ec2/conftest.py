import pytest

from sym.cli.helpers.ec2.client import Ec2Client, RunningInstance
from sym.cli.saml_clients.saml_client import SAMLClient

TEST_REGION = "test-region-1"
TEST_INSTANCE_ID = "i-0123456789abcdef"
TEST_IP = "10.20.30.40"
TEST_DNS_NAME = "ip-10-20-30-40.ec2.internal"
TEST_HOSTNAME = "test-host.com"
DEFAULT_REGION = "us-east-1"
TEST_INSTANCE = RunningInstance(instance_id=TEST_INSTANCE_ID, region=DEFAULT_REGION)

BOTO_EMPTY_RESPONSE = {"Reservations": []}
BOTO_INSTANCE_RESPONSE = {
    "Reservations": [
        {
            "Instances": [
                {
                    "InstanceId": TEST_INSTANCE_ID,
                }
            ]
        }
    ]
}


@pytest.fixture
def ec2_stub(boto_stub):
    return boto_stub("ec2")


@pytest.fixture
def ec2_client(saml_client: SAMLClient) -> Ec2Client:
    return Ec2Client(saml_client)


@pytest.fixture
def region(saml_client: SAMLClient) -> str:
    return saml_client.get_profile().region
