from pathlib import Path
from typing import List, Optional

from sym.cli.actions.sym_action import SymAction
from sym.cli.data.request_data import RequestData
from sym.cli.helpers.check.core import DependenciesCheck, SymCheck
from sym.cli.helpers.global_options import GlobalOptions
from sym.cli.helpers.ssh import maybe_gen_ssh_key
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory


class WriteCredsAction(SymAction):
    def __init__(self):
        super().__init__("write_creds")

    def get_requirements(self) -> List[SymCheck]:
        return [DependenciesCheck("aws"), DependenciesCheck("session-manager-plugin")]

    def execute(self, request_data: RequestData) -> None:
        """Extract specifications from request_data and trigger execution
        to write credentials to an AWS credentials file.
        """

        self.write_creds(
            request_data.resource,
            request_data.get_global_options(),
            request_data.params.get("path"),
            request_data.params.get("profile"),
            request_data.params.get("prefix"),
        )

    def write_creds(
        self,
        resource: str,
        options: GlobalOptions,
        path: Path,
        profile: Optional[str],
        prefix: str,
    ) -> None:
        """Write out approved credentials for the specified resource to the profile
        in the AWS credentials file at the specified path.
        """
        if not profile:
            profile = f"{prefix}-{resource}"
        client = SAMLClientFactory.create_saml_client(resource, options)
        client.write_creds(path=Path(path), profile=profile)
        maybe_gen_ssh_key(client)
