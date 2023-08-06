import datetime
from typing import Optional, Sequence

import pytest

from sym.cli.helpers.config import Config
from sym.cli.helpers.ec2.cache import CachingEc2Client
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.helpers.ec2.conftest import (
    BOTO_INSTANCE_RESPONSE,
    DEFAULT_REGION,
    TEST_INSTANCE,
    TEST_INSTANCE_ID,
    TEST_IP,
)
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture
def caching_ec2_client(saml_client: SAMLClient) -> CachingEc2Client:
    return CachingEc2Client(saml_client)


def assert_no_cached_instances():
    cached = Config.get_servers()
    assert len(cached) == 0


def assert_cache_miss(alias: str, caching_ec2_client: CachingEc2Client, ec2_stub):
    assert_no_cached_instances()
    ec2_stub.add_response(
        "describe_instances",
        BOTO_INSTANCE_RESPONSE,
    )
    instance = caching_ec2_client.load_instance_by_alias(alias)
    assert instance == TEST_INSTANCE
    ec2_stub.assert_no_pending_responses()


def assert_cache_hit(caching_ec2_client: CachingEc2Client):
    instance = caching_ec2_client.load_instance_by_alias(TEST_INSTANCE_ID)
    assert instance == TEST_INSTANCE


def assert_cached_instance(
    aliases: Sequence[str] = [],
    last_connection: Optional[datetime.datetime] = None,
    total_instances: int = 1,
):
    cached = Config.get_servers()
    assert len(cached) == total_instances

    cached_instance = cached[TEST_INSTANCE_ID]
    assert cached_instance["region"] == DEFAULT_REGION
    assert cached_instance["aliases"] == aliases
    assert cached_instance["last_connection"] == last_connection


def test_cache_miss_then_hit_id(
    sandbox: Sandbox, caching_ec2_client: CachingEc2Client, ec2_stub
):
    with sandbox.push_xdg_config_home():
        assert_cache_miss(TEST_INSTANCE_ID, caching_ec2_client, ec2_stub)
        assert_cached_instance()
        assert_cache_hit(caching_ec2_client)


def test_cache_miss_then_hit_by_ip(
    sandbox: Sandbox, caching_ec2_client: CachingEc2Client, ec2_stub
):
    with sandbox.push_xdg_config_home():
        assert_cache_miss(TEST_IP, caching_ec2_client, ec2_stub)
        assert_cached_instance(aliases=[TEST_IP])
        assert_cache_hit(caching_ec2_client)


TEST_MISSING_REGION_CACHED = f"""
email: r@symops.io
org: sym
servers:
  {TEST_INSTANCE_ID}:
    aliases:
      - {TEST_IP}
    last_connection: 2020-11-12 10:16:47.179202
"""


def test_cache_hit_with_missing_region(
    sandbox: Sandbox, caching_ec2_client: CachingEc2Client, ec2_stub
):
    with sandbox.push_xdg_config_home():
        with Config.instance().file as f:
            f.write(TEST_MISSING_REGION_CACHED)

        assert_cache_miss(TEST_INSTANCE_ID, caching_ec2_client, ec2_stub)
        assert_cached_instance(
            aliases=[TEST_IP],
            last_connection=datetime.datetime(2020, 11, 12, 10, 16, 47, 179202),
        )
        assert_cache_hit(caching_ec2_client)


TEST_NULL_REGION_CACHED = f"""
email: r@symops.io
org: sym
servers:
  {TEST_INSTANCE_ID}:
    aliases:
      - {TEST_IP}
    last_connection: 2020-11-12 10:16:47.179202
    region: null
"""


def test_cache_hit_with_null_region(
    sandbox: Sandbox, caching_ec2_client: CachingEc2Client, ec2_stub
):
    with sandbox.push_xdg_config_home():
        with Config.instance().file as f:
            f.write(TEST_NULL_REGION_CACHED)

        assert_cache_miss(TEST_INSTANCE_ID, caching_ec2_client, ec2_stub)
        assert_cached_instance(
            aliases=[TEST_IP],
            last_connection=datetime.datetime(2020, 11, 12, 10, 16, 47, 179202),
        )
        assert_cache_hit(caching_ec2_client)
