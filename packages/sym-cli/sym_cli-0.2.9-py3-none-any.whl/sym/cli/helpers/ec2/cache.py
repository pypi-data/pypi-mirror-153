from typing import Optional

from sym.cli.helpers.config import Config
from sym.cli.saml_clients.saml_client import SAMLClient

from .client import RunningInstance
from .multiregion import MultiRegionEc2Client


class CachingEc2Client(MultiRegionEc2Client):
    def __init__(self, client: SAMLClient):
        super().__init__(client)

    def _load_from_config(self, alias: str) -> Optional[RunningInstance]:
        """
        In the EC2 client, an alias could be an instance ID, IP address, or DNS name.
        Look for an instance in the config with an id that matches "alias", or with
        an entry in "aliases" that matches.
        """
        for instance_id, server in Config.get_servers().items():
            if region := server.get("region"):
                if alias == instance_id:
                    return RunningInstance(instance_id=alias, region=region)

                for known_alias in server.get("aliases", []):
                    if alias == known_alias:
                        return RunningInstance(instance_id=instance_id, region=region)
        return None

    def _store_to_config(self, alias: str, instance: RunningInstance):
        Config.record_instance(
            instance.instance_id,
            alias=alias if alias != instance.instance_id else None,
            region=instance.region,
        )

    def load_instance_by_alias(self, alias: str) -> RunningInstance:
        """
        The CachingEc2Client.load_instance_by_alias method first attempts
        to load the instance based on the local cached configuration.
        If the alias matches the instance ID, or is a member of the aliases
        list for an instance we have visited in the past, that will be returned.
        Otherwise, the instance is loaded by delegating to a MultiRegionEc2Client,
        then stored in the config before returning.
        """
        if existing := self._load_from_config(alias):
            return existing

        instance = super().load_instance_by_alias(alias)
        self._store_to_config(alias, instance)
        return instance
