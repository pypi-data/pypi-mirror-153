import re
import socket
from dataclasses import dataclass
from typing import List, Sequence

import boto3
import validators
from botocore.exceptions import ClientError

from sym.cli.errors import CliError, InstanceNotFound
from sym.cli.helpers import boto
from sym.cli.saml_clients.saml_client import SAMLClient

InstanceIDPattern = re.compile("^i-[a-f0-9]+$")
UnauthorizedError = re.compile(r"UnauthorizedOperation")
RequestExpired = re.compile(r"RequestExpired")


@dataclass
class RunningInstance:
    instance_id: str
    region: str

    def __repr__(self) -> str:
        return f"{self.instance_id} [{self.region}]"

    def __eq__(self, other: "RunningInstance") -> bool:
        return self.instance_id == other.instance_id and self.region == other.region


class InstanceQuery:
    def __init__(self):
        self.instance_ids = []
        self.filters = [{"Name": "instance-state-name", "Values": ["running"]}]

    def instance_id(self, instance_id: str) -> "InstanceQuery":
        self.instance_ids.append(instance_id)
        return self

    def filter(self, filter_key: str, filter_values: List[str]) -> "InstanceQuery":
        self.filters.append({"Name": filter_key, "Values": filter_values})
        return self

    def params(self) -> dict:
        return {"Filters": self.filters, "InstanceIds": self.instance_ids}


class InvalidQueryError(CliError):
    def __init__(self, msg):
        super().__init__(msg)


class Ec2Client:
    """
    A basic client for EC2 that wraps the boto library and exposes methods for loading EC2 regions
    and instances. Note that instances are only loaded from the region defined in the SAMLClient
    passed into the constructor. To load instances from region "foo", make sure the client has been
    set up using the region "foo".
    """

    def __init__(self, client: SAMLClient):
        self.client = client

    @boto.intercept_boto_errors
    def get_regions(self) -> Sequence[str]:
        """
        List all the regions for the current session. This will first try to load the regions using the current
        credentials and executing `ec2 describe_regions`. If that call fails, then this function will fallback to
        all available regions for a default boto session.
        """
        try:
            client = boto.boto_client(self.client, "ec2")
            regions = [
                region["RegionName"] for region in client.describe_regions()["Regions"]
            ]
        except ClientError as e:
            self.client.dprint(
                "error describing regions, falling back to default available regions in boto",
                error=e,
            )
            session = boto3.Session()
            regions = session.get_available_regions("ec2")

        return sorted(regions, key=lambda r: ("us" not in r, "eu" not in r, r))

    def load_instance_by_alias(self, alias: str) -> RunningInstance:
        """
        Load instance by an alias, which could be an instance ID, IP address, or DNS name.

        If the instance can't be found, then raise InstanceNotFound(alias)
        """
        if InstanceIDPattern.match(alias):
            return self._load_instance(
                InstanceQuery().instance_id(alias),
                alias,
            )
        elif validators.ip_address.ipv4(alias):
            return self._load_instance_by_first_filter(
                ["ip-address", "private-ip-address"], alias
            )
        else:
            return self._load_instance_by_dns(alias)

    def _load_instance_by_dns(self, alias: str) -> RunningInstance:
        try:
            return self._load_instance_by_first_filter(
                ["dns-name", "private-dns-name"], alias
            )
        except InstanceNotFound as not_found:
            try:
                ip_addr = socket.gethostbyname(alias)
            except socket.error as e:
                self.client.dprint(
                    "Exception trying to resolve alias", alias=alias, error=e
                )
                raise not_found

            try:
                return self.load_instance_by_alias(ip_addr)
            except InstanceNotFound as e:
                self.client.dprint(
                    "Resolved alias into IP, but could not find instance by IP",
                    alias=alias,
                    ip_addr=ip_addr,
                )
                raise not_found

    @boto.intercept_boto_errors
    def _load_instances(self, query: InstanceQuery) -> List[RunningInstance]:
        """
        Load 0 or more instances by executing the supplied query. If the underlying
        call returns InvalidInstanceID.NotFound, because the query contains an unknown
        instance ID, then this function raises InstanceNotFound.
        """
        found = []
        client = boto.boto_client(self.client, "ec2")
        paginator = client.get_paginator("describe_instances")
        try:
            for response in paginator.paginate(
                Filters=query.filters,
                InstanceIds=query.instance_ids,
            ):
                for reservation in response["Reservations"]:
                    for instance in reservation["Instances"]:
                        found.append(
                            RunningInstance(
                                instance_id=instance["InstanceId"],
                                region=client.meta.region_name,
                            )
                        )
            return found
        except ClientError as e:
            if e.response["Error"]["Code"] == "InvalidInstanceID.NotFound":
                raise InstanceNotFound(query.instance_ids)
            raise

    def _load_instance(
        self, query: InstanceQuery, alias_for_errors: str
    ) -> RunningInstance:
        """
        Load exactly one instance by executing the supplied query.
        If the query returns 0 instances, this function raises InstanceNotFound.
        If the query returns 2 or more instances, this function raises InvalidQueryError.
        If the query raises an InstanceNotFound error, this function passes it.
        Otherwise, return the sole instance from the query result.
        """
        instances = self._load_instances(query)
        if len(instances) == 0:
            raise InstanceNotFound(alias_for_errors)
        elif len(instances) > 1:
            raise InvalidQueryError(
                f"Expected at most 1 instance matching {alias_for_errors}"
            )
        else:
            return instances[0]

    def _load_instance_by_first_filter(
        self, filter_keys: List[str], filter_value: str
    ) -> RunningInstance:
        """
        Load exactly one instance by searching against the set of filter_keys for the
        specified filter_value. The function stops when one of the filter key and value pairs
        matches an instance. If none match, this function raises TargetNotFound. If the underlying
        query returns InvalidQueryError, this function passes it.

        A common use case would be searching multiple fields ("ip-address", private-ip-address")
        for a particular IP address alias match. Returns immediately after finding a match in either key.
        """
        for key in filter_keys:
            try:
                return self._load_instance(
                    InstanceQuery().filter(key, [filter_value]),
                    filter_value,
                )
            except InstanceNotFound:
                pass

        raise InstanceNotFound(filter_value)
