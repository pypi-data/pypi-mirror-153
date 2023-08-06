import re
import shlex
import sys
from abc import ABC, abstractmethod
from configparser import ConfigParser
from datetime import datetime, timedelta
from operator import attrgetter
from pathlib import Path
from typing import ClassVar, Optional, Sequence, Type
from urllib.parse import urlsplit

import click
import dateutil.parser
from policyuniverse.arn import ARN
from sym.shared.cli.helpers import segment
from sym.shared.cli.helpers.config import SymConfigFile
from sym.shared.cli.helpers.keywords_to_options import keywords_to_options
from sym.shared.cli.helpers.os import read_write_lock

from sym.cli.helpers import validations
from sym.cli.helpers.params import Profile, get_aws_saml_url, get_profile


class SAMLClient(ABC):
    binary: ClassVar[str]
    option_value: ClassVar[str]
    priority: ClassVar[int]
    setup_help: ClassVar[Optional[str]] = None

    resource: str
    options: "GlobalOptions"

    config_file: SymConfigFile

    _config: Optional[ConfigParser]
    _session_exists: bool
    _checked_setup: bool

    def __init__(self, resource: str, *, options: "GlobalOptions") -> None:
        self.resource = resource
        self.options = options

        self._config = None
        self._session_exists = False
        self._checked_setup = False

        self.check_is_setup()
        options.saml_clients[resource] = self

    @property
    def _section_name(self):
        return f"sym-{self.resource}"

    @property
    def debug(self):
        return self.options.debug

    @property
    def log_dir(self):
        return self.options.log_dir

    @property
    def session_length(self) -> Optional[int]:
        return self.options.session_length

    @classmethod
    def validate_resource(cls, resource: str):
        return validations.validate_resource(resource)

    def check_is_setup(self):
        if self._checked_setup:
            return
        self._checked_setup = True

        if self.is_setup():
            return

        click.secho(
            f"Warning: sym might not function correctly until {self.binary} is setup.",
            err=True,
            fg="yellow",
            bold=True,
        )
        if self.setup_help:
            click.secho(f"Hint: {self.setup_help}\n", err=True, fg="cyan", bold=True)

    @classmethod
    def sorted_subclasses(cls):
        filtered_subclasses = [
            c for c in cls.__subclasses__() if "Test" not in c.__name__
        ]
        return sorted(filtered_subclasses, key=attrgetter("priority"), reverse=True)

    @abstractmethod
    def _exec(self, *args: str, **opts: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def _ensure_config(self, profile: Profile) -> ConfigParser:
        raise NotImplementedError

    @abstractmethod
    def is_setup(self) -> bool:
        raise NotImplementedError

    def _cli_options(self):
        return {
            "saml_client": self.option_value,
            "debug": self.debug,
            "log_dir": self.log_dir,
        }

    @property
    def cli_options(self):
        return shlex.join(keywords_to_options([self._cli_options()]))

    def exec(self, *args: str, **kwargs: str) -> None:
        self.ensure_session()
        self.dprint(f"client: {self.cli_options}")
        return self._exec(*args, **kwargs)

    def _ensure_session(self, *, force: bool):
        self.dprint(f"ensuring session, force={force}")
        self._exec(
            "true",
            silence_stderr_=False,
            suppress_=True,
            run_subprocess_options_=self.options,
            intercept_errors_options_=self.options,
        )

    def ensure_session(self, force=False):
        if not self._session_exists:
            self._ensure_session(force=force or self._creds_expiring())
            self._session_exists = True

    def ensure_config(self) -> ConfigParser:
        if not self._config:
            config = self._ensure_config(self.get_profile())
            with self.config_file as f:
                config.write(f)
            self.dconfig(config)
            self._config = config
        return self._config

    def subconfig(self, file_name, **deps):
        return SymConfigFile(
            **self._cli_options(), resource=self.resource, **deps, file_name=file_name
        )

    def dprint(self, *s: Sequence[str], **kwargs):
        self.options.dprint(*s, **kwargs)

    def dconfig(self, config: ConfigParser):
        if self.debug:
            print("Writing config:", file=sys.stderr)
            config.write(sys.stderr)

    def log_subprocess_event(self, command: tuple):
        segment.track("Subprocess Called", global_options=self.options, binary=command[0])

    def get_profile(self) -> Profile:
        profile = get_profile(self.resource)
        self.dprint(f"Using profile {profile}")
        return profile

    def get_aws_saml_url(self, bare: bool = False) -> str:
        url = get_aws_saml_url(self.resource)
        if bare:
            url = urlsplit(url).path[1:]
        return url

    @property
    def _cred_env_vars(self):
        return (
            "AWS_REGION",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_SESSION_TOKEN",
            "AWS_SECURITY_TOKEN",
            "AWS_CREDENTIAL_EXPIRATION",
        )

    def get_creds(self):
        output = self._exec(
            "env",
            capture_output_=True,
            censor_=True,
            run_subprocess_options_=self.options,
            intercept_errors_options_=self.options,
        )[-1]
        env_vars = re.findall(r"([\w_]+)=(.+)\n", output)
        return {k: v for k, v in env_vars if k in self._cred_env_vars}

    def has_creds(self) -> bool:
        try:
            self.get_creds()
            return True
        except Exception:
            return False

    def _creds_expiring(self, buffer=timedelta(minutes=2)):
        try:
            creds = self.get_creds()
        except Exception:
            return True

        if expires := creds.get("AWS_CREDENTIAL_EXPIRATION"):
            try:
                parsed = dateutil.parser.isoparse(expires)
            except ValueError:
                return True  # Assume they are expiring as we're not sure
            remaining = parsed - datetime.now(parsed.tzinfo)
            self.dprint(f"{remaining} remaining in creds session")
            return remaining < buffer
        return False

    def _profile_matches_caller_identity(self):
        from sym.cli.helpers.boto import get_identity

        profile = self.get_profile()
        if not profile.arn:
            return False
        profile_role = self.resource_from_arn(profile.arn)

        caller_identity = get_identity(self)
        caller_resource = self.resource_from_arn(caller_identity["Arn"])

        self.dprint(f"*** Caller Resource Name: {caller_resource}")
        self.dprint(f"*** Profile Role Name: {profile_role}")

        if not set(profile_role.split("/")) < set(caller_resource.split("/")):
            self.dprint(f"*** Caller identity does not match profile user!")
            return False

        return True

    def resource_from_arn(self, arn):
        if not arn:
            raise ValueError("SAMLClient missing ARN")

        name = ARN(arn).name
        if "/" in name:
            name = name.split("/", 1)[1]
        elif ":" in name:
            name = name.split(":", 1)[1]
        return name

    def write_creds(self, *, path: Path, profile: str):
        self.dprint(f"writing creds, profile={profile}")

        if (
            self._creds_expiring(
                buffer=timedelta(minutes=(self.session_length or 30) / 3)
            )
            or not self._profile_matches_caller_identity()
        ):
            self._ensure_session(force=True)

        creds = self.get_creds()
        creds["region"] = creds.pop("AWS_REGION", self.get_profile().region)
        creds["x_security_token_expires"] = creds.pop("AWS_CREDENTIAL_EXPIRATION", None)
        creds["x_sym_ansible_bucket"] = self.get_profile().ansible_bucket

        path.parent.mkdir(parents=True, exist_ok=True)

        with read_write_lock(path) as f:
            config = ConfigParser(strict=False)
            config.read_file(f)

            if config.has_section(profile):
                config.remove_section(profile)
            config.add_section(profile)
            for k, v in creds.items():
                if v:
                    config.set(profile, k.lower(), v)

            f.seek(0)
            f.truncate()
            config.write(f)

    def clone(self, *, klass: Type["SAMLClient"] = None, **overrides):
        kwargs = {
            key: overrides.get(key, getattr(self, key)) for key in ["resource", "options"]
        }
        return (klass or self.__class__)(**kwargs)

    def send_analytics_event(self):
        segment.track(
            "Resource Accessed",
            global_options=self.options,
            resource=self.resource,
        )
