import socket

import pytest
from sym.shared.cli.tests.conftest import MonkeyPatch

from sym.cli.errors import InstanceNotFound
from sym.cli.helpers.ec2.client import Ec2Client, InstanceQuery, InvalidQueryError
from sym.cli.tests.helpers.ec2.conftest import (
    BOTO_EMPTY_RESPONSE,
    BOTO_INSTANCE_RESPONSE,
    TEST_DNS_NAME,
    TEST_HOSTNAME,
    TEST_INSTANCE,
    TEST_INSTANCE_ID,
    TEST_IP,
    TEST_REGION,
)


def test_get_regions(ec2_stub, ec2_client):
    ec2_stub.add_response(
        "describe_regions",
        {"Regions": [{"RegionName": TEST_REGION}]},
    )
    regions = ec2_client.get_regions()
    assert regions == [TEST_REGION]


def test_get_regions_boto_error_fallback(ec2_stub, ec2_client: Ec2Client):
    ec2_stub.add_client_error(
        "describe_regions",
        service_message="Error describing regions",
        http_status_code=400,
    )
    regions = ec2_client.get_regions()
    assert len(regions) == 22
    assert "us-east-1" in regions


def test_load_instance_by_id(ec2_stub, ec2_client: Ec2Client):
    ec2_stub.add_response(
        "describe_instances",
        BOTO_INSTANCE_RESPONSE,
        InstanceQuery().instance_id(TEST_INSTANCE_ID).params(),
    )
    instance = ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
    assert instance == TEST_INSTANCE


def test_load_instance_by_id_boto_error(ec2_stub, ec2_client: Ec2Client):
    with pytest.raises(InstanceNotFound, match=TEST_INSTANCE_ID):
        ec2_stub.add_client_error(
            "describe_instances",
            service_message="Error describing instances",
            service_error_code="InvalidInstanceID.NotFound",
            http_status_code=400,
        )
        ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)


def test_load_instance_by_id_no_res(ec2_stub, ec2_client: Ec2Client):
    with pytest.raises(InstanceNotFound, match=TEST_INSTANCE_ID):
        ec2_stub.add_response(
            "describe_instances",
            {"Reservations": []},
            InstanceQuery().instance_id(TEST_INSTANCE_ID).params(),
        )
        ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)


def test_load_instance_by_id_no_inst(ec2_stub, ec2_client: Ec2Client):
    with pytest.raises(InstanceNotFound, match=TEST_INSTANCE_ID):
        ec2_stub.add_response(
            "describe_instances",
            {"Reservations": [{"Instances": []}]},
            InstanceQuery().instance_id(TEST_INSTANCE_ID).params(),
        )
        ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)


def test_load_instance_by_id_too_many_inst(ec2_stub, ec2_client: Ec2Client):
    with pytest.raises(InvalidQueryError, match=TEST_INSTANCE_ID):
        ec2_stub.add_response(
            "describe_instances",
            {
                "Reservations": [
                    {
                        "Instances": [
                            {"InstanceId": TEST_INSTANCE_ID},
                            {"InstanceId": "foo"},
                        ]
                    }
                ]
            },
            InstanceQuery().instance_id(TEST_INSTANCE_ID).params(),
        )
        ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)


def test_load_instance_by_private_ip(ec2_stub, ec2_client: Ec2Client):
    ec2_stub.add_response(
        "describe_instances",
        BOTO_INSTANCE_RESPONSE,
        InstanceQuery().filter("ip-address", [TEST_IP]).params(),
    )
    instance = ec2_client.load_instance_by_alias(TEST_IP)
    assert instance == TEST_INSTANCE


def test_load_instance_by_private_ip_no_inst(ec2_stub, ec2_client: Ec2Client):
    with pytest.raises(InstanceNotFound, match=TEST_IP):
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("ip-address", [TEST_IP]).params(),
        )
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("private-ip-address", [TEST_IP]).params(),
        )
        ec2_client.load_instance_by_alias(TEST_IP)


def test_load_instance_by_private_dns(ec2_stub, ec2_client: Ec2Client):
    ec2_stub.add_response(
        "describe_instances",
        BOTO_INSTANCE_RESPONSE,
        InstanceQuery().filter("dns-name", [TEST_DNS_NAME]).params(),
    )
    instance = ec2_client.load_instance_by_alias(TEST_DNS_NAME)
    assert instance == TEST_INSTANCE


def test_load_instance_by_dns_socket_error(
    ec2_stub, ec2_client: Ec2Client, monkeypatch: MonkeyPatch
):
    mock = {"called": False}

    def get_host(_: str) -> str:
        mock["called"] = True
        raise socket.gaierror(1, "")

    monkeypatch.setattr(socket, "gethostbyname", get_host)

    with pytest.raises(InstanceNotFound, match=TEST_HOSTNAME):
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("dns-name", [TEST_HOSTNAME]).params(),
        )
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("private-dns-name", [TEST_HOSTNAME]).params(),
        )
        ec2_client.load_instance_by_alias(TEST_HOSTNAME)

    assert mock["called"]


def test_load_instance_by_dns_lookup_then_ip_unknown(
    ec2_stub, ec2_client: Ec2Client, monkeypatch: MonkeyPatch
):
    def get_host(_: str) -> str:
        return TEST_IP

    monkeypatch.setattr(socket, "gethostbyname", get_host)

    with pytest.raises(InstanceNotFound, match=TEST_HOSTNAME):
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("dns-name", [TEST_HOSTNAME]).params(),
        )
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("private-dns-name", [TEST_HOSTNAME]).params(),
        )
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("ip-address", [TEST_IP]).params(),
        )
        ec2_stub.add_response(
            "describe_instances",
            BOTO_EMPTY_RESPONSE,
            InstanceQuery().filter("private-ip-address", [TEST_IP]).params(),
        )
        ec2_client.load_instance_by_alias(TEST_HOSTNAME)


def test_load_instance_by_dns_lookup_then_ip_success(ec2_stub, ec2_client: Ec2Client):
    ec2_stub.add_response(
        "describe_instances",
        BOTO_EMPTY_RESPONSE,
        InstanceQuery().filter("dns-name", ["localhost"]).params(),
    )
    ec2_stub.add_response(
        "describe_instances",
        BOTO_EMPTY_RESPONSE,
        InstanceQuery().filter("private-dns-name", ["localhost"]).params(),
    )
    ec2_stub.add_response(
        "describe_instances",
        BOTO_INSTANCE_RESPONSE,
        InstanceQuery().filter("ip-address", ["127.0.0.1"]).params(),
    )
    instance = ec2_client.load_instance_by_alias("localhost")
    assert instance == TEST_INSTANCE
