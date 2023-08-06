from sym.cli.actions.sym_action import SymAction
from sym.cli.data.request_data import RequestData
from sym.cli.errors import CliError


class ActionRegistry:
    """
    Jumping off point to execute specific actions.  Note that overall this class has minimal
    dependencies.  It establishes a fixed strategy to:
        - Validate inputs
        - Load dependencies
        - Execute the referenced action
        - Log status and errors
    """

    @classmethod
    def create_ssh_action(cls) -> SymAction:
        from sym.cli.actions.ssh_session_action import SSHSessionAction

        return SSHSessionAction()

    @classmethod
    def create_write_creds_action(cls) -> SymAction:
        from sym.cli.actions.write_creds_action import WriteCredsAction

        return WriteCredsAction()

    @classmethod
    def create_ansible_action(cls) -> SymAction:
        from sym.cli.actions.ansible_action import AnsibleAction

        return AnsibleAction()

    @classmethod
    def create_ansible_playbook_action(cls) -> SymAction:
        from sym.cli.actions.ansible_playbook_action import AnsiblePlaybookAction

        return AnsiblePlaybookAction()

    @classmethod
    def instantiate_plugin(cls, action_name) -> SymAction:
        if action_name == "ssh_session":
            return cls.create_ssh_action()
        elif action_name == "write_creds":
            return cls.create_write_creds_action()
        elif action_name == "ansible":
            return cls.create_ansible_action()
        elif action_name == "ansible_playbook":
            return cls.create_ansible_playbook_action()

        raise CliError(f"unknown command: {action_name}")

    @classmethod
    def execute(cls, request_data: RequestData):
        """
        Note: This interface is a work in progress.  Right now it serves to call out to our action,
        but in the end I'd like to return an ExecutionScope object that does not exist.
        :param request_data:
        :return:
        """
        action = cls.instantiate_plugin(request_data.action)
        action.validate_inputs(request_data)
        action.invoke_requirements()
        return action.execute(request_data)
