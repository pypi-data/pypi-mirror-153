from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List, Mapping, MutableMapping, Optional, TypedDict

import immutables
from sym.shared.cli.helpers.config import SymConfigFile, init  # noqa
from sym.shared.cli.helpers.config.base import ConfigBase, fail_ok


class ServerConfigSchema(TypedDict):
    region: Optional[str]
    last_connection: Optional[datetime]
    aliases: List[str]


class ConfigSchema(TypedDict, total=False):
    org: str
    email: str
    default_resource: str
    last_update_check: Optional[datetime]
    servers: MutableMapping[str, ServerConfigSchema]
    autoupdate: Optional[str]
    analytics: Optional[str]


class Config(ConfigBase[ConfigSchema]):
    @classmethod
    def get_org(cls) -> str:
        return cls.instance()["org"]

    @classmethod
    def get_handle(cls) -> str:
        return cls.get_email().split("@")[0]

    @classmethod
    def get_servers(cls) -> Mapping[str, ServerConfigSchema]:
        return cls.instance().get("servers", immutables.Map())

    @classmethod
    def get_instance(cls, instance: str) -> Optional[ServerConfigSchema]:
        return cls.get_servers().get(instance)

    @classmethod
    def find_instance_by_alias(
        cls, alias: str, ttl: timedelta = timedelta(days=1)
    ) -> Optional[str]:
        for instance, config in cls.get_servers().items():
            if alias in config.get("aliases", []) and cls.check_instance_ttl(
                instance,
                ttl,
                allow_new=True,
            ):
                return instance

    @classmethod
    def check_instance_ttl(
        cls,
        instance: str,
        ttl: timedelta = timedelta(days=1),
        allow_new=False,
    ) -> bool:
        instance_config = cls.get_instance(instance)
        if not instance_config:
            return allow_new
        last_connect = instance_config.get("last_connection")
        if not last_connect:
            return allow_new
        return datetime.now() - last_connect < ttl

    @classmethod
    @contextmanager
    def _atomic_instance_mutation(cls, instance: str):
        with cls.instance().atomic():
            instance_config = cls.get_instance(instance)
            if not instance_config:
                instance_config = ServerConfigSchema(
                    last_connection=None, region=None, aliases=[]
                )
            yield instance_config
            cls.instance()["servers"] = cls.get_servers().set(instance, instance_config)

    @classmethod
    @fail_ok
    def touch_instance(cls, instance: str, error: bool = False):
        with cls._atomic_instance_mutation(instance) as instance_config:
            if error:
                instance_config["last_connection"] = datetime.now() - timedelta(weeks=52)
                instance_config["aliases"] = []
            else:
                instance_config["last_connection"] = datetime.now()

    @classmethod
    @fail_ok
    def add_instance_alias(cls, instance: str, *, alias: str, region: str):
        if old_instance := cls.find_instance_by_alias(alias):
            with cls._atomic_instance_mutation(old_instance) as instance_config:
                instance_config["aliases"].remove(alias)

        with cls._atomic_instance_mutation(instance) as instance_config:
            if "aliases" not in instance_config:
                instance_config["aliases"] = []
            if alias not in instance_config["aliases"]:
                instance_config["aliases"].append(alias)
            if region:
                instance_config["region"] = region

    @classmethod
    @fail_ok
    def record_instance(cls, instance_id: str, *, alias: str, region: str):
        with cls._atomic_instance_mutation(instance_id) as instance_config:
            if alias:
                instance_config["aliases"].append(alias)
            if region:
                instance_config["region"] = region
