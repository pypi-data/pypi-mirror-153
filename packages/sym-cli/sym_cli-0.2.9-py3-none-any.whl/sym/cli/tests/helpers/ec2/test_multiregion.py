import pytest

from sym.cli.helpers.ec2.client import InstanceNotFound
from sym.cli.helpers.ec2.multiregion import MultiRegionEc2Client
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.helpers.ec2.conftest import (
    BOTO_EMPTY_RESPONSE,
    BOTO_INSTANCE_RESPONSE,
    TEST_INSTANCE,
    TEST_INSTANCE_ID,
    TEST_REGION,
)


@pytest.fixture
def multiregion_ec2_client(saml_client: SAMLClient) -> MultiRegionEc2Client:
    return MultiRegionEc2Client(saml_client)


def test_multiregion_find_in_other_region(
    ec2_stub, multiregion_ec2_client, click_context
):
    with click_context:
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
        )
        ec2_stub.add_response(
            "describe_regions",
            {"Regions": [{"RegionName": TEST_REGION}]},
        )
        ec2_stub.add_response(
            "describe_instances",
            BOTO_INSTANCE_RESPONSE,
        )
        instance = multiregion_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
        assert instance == TEST_INSTANCE


def test_multiregion_find_in_default(ec2_stub, multiregion_ec2_client, click_context):
    with click_context:
        ec2_stub.add_response(
            "describe_instances",
            BOTO_INSTANCE_RESPONSE,
        )
        instance = multiregion_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
        assert instance == TEST_INSTANCE


def test_multiregion_not_found(ec2_stub, multiregion_ec2_client, click_context):
    with pytest.raises(InstanceNotFound, match=TEST_INSTANCE_ID):
        with click_context:
            ec2_stub.add_response(
                "describe_instances",
                BOTO_EMPTY_RESPONSE,
            )
            ec2_stub.add_response(
                "describe_regions",
                {"Regions": [{"RegionName": TEST_REGION}]},
            )
            ec2_stub.add_response(
                "describe_instances",
                BOTO_EMPTY_RESPONSE,
            )
            multiregion_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
