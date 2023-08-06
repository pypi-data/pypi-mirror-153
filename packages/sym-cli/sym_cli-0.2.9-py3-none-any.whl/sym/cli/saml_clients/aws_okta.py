import re
import sys
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path
from typing import Final, Iterator, Optional, Tuple
from urllib.parse import urlsplit

import keyring
from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.helpers.keywords_to_options import Argument

from sym.cli.helpers.constants import AwsOktaNoCreds, AwsOktaNoRoles, AwsOktaNotSetup

from ..decorators import intercept_errors, require_bins, run_subprocess
from ..errors import (
    FailedSubprocessError,
    ResourceNotSetup,
    SamlClientNotSetup,
    UnavailableResourceError,
)
from ..helpers.config import Config, SymConfigFile
from ..helpers.params import Profile, get_aws_okta_params
from .saml_client import SAMLClient

ErrorPatterns = {
    AwsOktaNoRoles: UnavailableResourceError,
    AwsOktaNotSetup: ResourceNotSetup,
    AwsOktaNoCreds: SamlClientNotSetup,
}

SessionIDPattern = re.compile(r"cache get `(.*)`")


class AwsOkta(SAMLClient):
    __slots__ = ["config_file", "resource", "options", "_config"]
    binary = "aws-okta"
    option_value = "aws-okta"
    priority = 5
    setup_help = "Run `aws-okta add`."

    resource: str
    options: "GlobalOptions"
    config_file: Final[SymConfigFile]
    _config: Optional[ConfigParser]

    def __init__(self, resource: str, *, options: "GlobalOptions") -> None:
        super().__init__(resource, options=options)
        self.config_file = SymConfigFile(resource=resource, file_name="aws-okta.cfg")

    def is_setup(self) -> bool:
        path = Path.home() / ".aws" / "config"
        config = ConfigParser(strict=False)
        config.read(path)
        return "okta" in config.sections()

    @property
    def _cred_env_vars(self):
        return super()._cred_env_vars + ("AWS_OKTA_SESSION_EXPIRATION",)

    def get_creds(self):
        creds = super().get_creds()
        creds["AWS_CREDENTIAL_EXPIRATION"] = (
            datetime.fromtimestamp(int(creds["AWS_OKTA_SESSION_EXPIRATION"]))
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )
        return creds

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @require_bins(binary)
    def _exec(
        self, *args: str, debug_: bool = False, **opts: str
    ) -> Iterator[Tuple[Argument, ...]]:
        self.ensure_config()
        with push_env("AWS_CONFIG_FILE", str(self.config_file)):
            yield (
                "aws-okta",
                {"debug": self.debug or debug_},
                "exec",
                self._section_name,
                "--",
                *args,
                opts,
            )

    def _get_session_id(self):
        try:
            self._exec(
                "false",
                capture_output_=True,
                debug_=True,
                run_subprocess_options_=self.options,
                intercept_errors_options_=self.options,
            )
        except FailedSubprocessError as err:
            if match := SessionIDPattern.search(err.__cause__.stderr):
                return match[1]

    def _clear_session(self):
        if session_id := self._get_session_id():
            print(
                (
                    "Your credentials are about to expire."
                    "\nDue to a bug in aws-okta,"
                    " sym will now clear your cached credentials and request new ones."
                ),
                file=sys.stderr,
            )
            try:
                keyring.delete_password("aws-okta-login", session_id)
            except keyring.errors.KeyringError:
                pass

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @require_bins(binary)
    def _login(self) -> Iterator[Tuple[Argument, ...]]:
        self.ensure_config()
        with push_env("AWS_CONFIG_FILE", str(self.config_file)):
            yield (
                "aws-okta",
                {"debug": self.debug},
                "add",
                {"domain": self.okta_domain, "username": Config.get_email()},
                {
                    k: v
                    for k, v in get_aws_okta_params().items()
                    if k in ["mfa_provider", "mfa_factor_type"]
                },
            )

    def _ensure_session(self, *, force: bool):
        if force:
            self._clear_session()
        # aws-okta fails in mysterious ways if your
        # keychain credentials are deleted after setup.
        # This logic handles that case cleanly.
        try:
            super()._ensure_session(force=force)
        except FailedSubprocessError:
            print("Logging in to Okta...", file=sys.stderr)
            self._login(silence_stderr_=False)
            print("Fetching SAML assertion...", file=sys.stderr)
            super()._ensure_session(force=force)

    @property
    def okta_domain(self) -> str:
        url = self.get_aws_saml_url(bare=False)
        return urlsplit(url).netloc

    @property
    def _session_ttl(self) -> Optional[str]:
        if self.session_length:
            return f"{self.session_length}m"
        return get_aws_okta_params().get("session_ttl")

    def _ensure_config(self, profile: Profile) -> ConfigParser:
        config = ConfigParser(default_section="okta")
        config.read_dict(
            {
                "okta": get_aws_okta_params(),
                f"profile {self._section_name}": {
                    "aws_saml_url": self.get_aws_saml_url(bare=True),
                    "region": profile.region,
                    "role_arn": profile.arn,
                    **get_aws_okta_params(),
                    "session_ttl": self._session_ttl,
                },
            }
        )
        return config
