import os
from configparser import ConfigParser
from functools import cached_property
from pathlib import Path
from typing import Iterator, Tuple

from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.helpers.keywords_to_options import Argument

from sym.cli.helpers.boto import get_identity

from ..decorators import command_require_bins, intercept_errors, run_subprocess
from ..errors import InvalidResource
from ..helpers.params import Profile
from .saml_client import SAMLClient

AwsCredentialsPath = Path(
    os.getenv("AWS_CREDENTIAL_FILE", Path.home() / ".aws" / "credentials")
)


class AwsProfile(SAMLClient):
    binary = "aws"
    option_value = "aws-profile"
    priority = 0
    setup_help = f"Set up your profile in `{str(AwsCredentialsPath)}`."

    resource: str
    options: "GlobalOptions"

    @classmethod
    def _read_creds_config(cls):
        config = ConfigParser(strict=False)
        config.read(AwsCredentialsPath)
        return config

    @classmethod
    def validate_resource(cls, resource: str):
        config = cls._read_creds_config()
        return config.has_section(resource)

    @cached_property
    def _section(self):
        config = self.__class__._read_creds_config()
        return config[self.resource]

    def raise_if_invalid(self):
        if self.__class__.validate_resource(self.resource):
            return
        raise InvalidResource(
            self.resource, self.__class__._read_creds_config().sections()
        )

    def get_creds(self):
        creds = {k.upper(): v for k, v in self._section.items() if k.startswith("aws")}
        creds["AWS_REGION"] = self._section.get("region")
        creds["AWS_CREDENTIAL_EXPIRATION"] = self._section.get("x_security_token_expires")
        return creds

    @intercept_errors()
    @run_subprocess
    @command_require_bins(binary)
    def _exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        with push_env("AWS_PROFILE", self.resource):
            yield (*args, opts)

    def is_setup(self) -> bool:
        return AwsCredentialsPath.exists()

    def _ensure_config(self, profile: Profile) -> ConfigParser:
        return ConfigParser(strict=False)

    def _ensure_session(self, *, force: bool):
        if not force and not self._creds_expiring():
            return
        get_identity(self)

    def get_profile(self):
        return Profile(
            display_name=self.resource,
            region=self._section.get("region"),
            arn=self._section.get("x_principal_arn"),
            ansible_bucket=self._section.get("x_sym_ansible_bucket"),
        )

    def send_analytics_event(self):
        pass
