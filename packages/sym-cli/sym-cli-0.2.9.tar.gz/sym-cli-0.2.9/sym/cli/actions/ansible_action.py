from typing import List

from sym.cli.actions.sym_action import SymAction
from sym.cli.data.request_data import RequestData
from sym.cli.helpers.ansible import run_ansible
from sym.cli.helpers.check.core import DependenciesCheck, SymCheck
from sym.cli.saml_clients.saml_client_factory import SAMLClientFactory


class AnsibleAction(SymAction):
    def __init__(self):
        super().__init__("ansible")

    def get_requirements(self) -> List[SymCheck]:
        return [DependenciesCheck("aws"), DependenciesCheck("session-manager-plugin")]

    def execute(self, request_data: RequestData):
        """Extract specifications from request_data and trigger execution
        to run an Ansible command against an inventory of EC2 instances.
        """
        global_options = request_data.get_global_options()
        ansible_options = request_data.get_ansible_options()

        client = SAMLClientFactory.create_saml_client(
            request_data.resource, global_options
        )
        client.send_analytics_event()

        run_ansible(
            client,
            ansible_options.command,
            ansible_aws_profile=ansible_options.ansible_aws_profile,
            ansible_sym_resource=ansible_options.ansible_sym_resource,
            control_master=ansible_options.control_master,
            send_command=ansible_options.send_command,
            forks=ansible_options.forks,
            ssm_timeout=ansible_options.ssm_timeout,
        )
