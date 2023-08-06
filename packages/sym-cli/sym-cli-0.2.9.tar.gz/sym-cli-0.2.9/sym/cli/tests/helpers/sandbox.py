from contextlib import contextmanager
from typing import Optional

from sym.shared.cli.helpers.config.base import ConfigBase
from sym.shared.cli.tests.helpers.sandbox import Sandbox as SharedSandbox

from sym.cli.helpers.config import Config
from sym.cli.saml_clients.aws_okta import AwsOkta


class Sandbox(SharedSandbox):
    def reset_config(self):
        ConfigBase.reset()
        Config.reset()

    @contextmanager
    def setup(self, set_org: Optional[bool] = True, set_client: Optional[bool] = True):
        with self.push_xdg_config_home():
            if set_client:
                self.create_binary(f"bin/{AwsOkta.binary}")
            with self.push_exec_path():
                if set_org:
                    Config.instance()["org"] = "sym"
                    Config.instance()["email"] = "y@symops.io"
                yield
