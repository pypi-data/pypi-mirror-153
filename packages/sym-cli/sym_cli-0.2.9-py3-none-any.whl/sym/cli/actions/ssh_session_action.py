from typing import List

from sym.cli.actions.sym_action import SymAction
from sym.cli.data.request_data import RequestData
from sym.cli.helpers.check.core import DependenciesCheck, SymCheck
from sym.cli.helpers.ec2.factory import get_ec2_client
from sym.cli.helpers.ssh import ensure_public_key_on_instance, start_tunnel
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory


class SSHSessionAction(SymAction):
    def __init__(self):
        super().__init__("ssh_session")

    def get_requirements(self) -> List[SymCheck]:
        return [DependenciesCheck("aws"), DependenciesCheck("session-manager-plugin")]

    def execute(self, request_data: RequestData):
        """Use approved creds for RESOURCE to tunnel a SSH session through an SSM session."""
        client = SAMLClientFactory.create_saml_client(
            request_data.resource, request_data.get_global_options()
        )

        target_options = request_data.get_target_options()
        running_instance = get_ec2_client(client).load_instance_by_alias(
            target_options.host
        )

        new_client = SAMLClientFactory.clone(client, aws_region=running_instance.region)
        if request_data.params["ensure_key"]:
            ensure_public_key_on_instance(
                client, running_instance.instance_id, target_options.port
            )
        start_tunnel(new_client, running_instance.instance_id, target_options.port)
