from typing import Dict

from sym.cli.data.ansible_options import AnsibleOptions
from sym.cli.data.target_options import TargetOptions
from sym.cli.helpers.global_options import GlobalOptions


class OptionsType:
    REQUEST = "Request"
    TARGET = "Target"
    ANSIBLE = "Ansible"


class RequestData:
    def __init__(
        self,
        action: str,
        resource: str,
        global_options: GlobalOptions = None,
        target_options: TargetOptions = None,
        ansible_options: AnsibleOptions = None,
        params: Dict = None,
    ):
        self.action = action
        self.resource = resource
        self.options = {}
        self.params = params or {}

        if global_options:
            self.set_options(OptionsType.REQUEST, global_options)

        if target_options:
            self.set_options(OptionsType.TARGET, target_options)

        if ansible_options:
            self.set_options(OptionsType.ANSIBLE, ansible_options)

    def get_options(self, key):
        return self.options.get(key, None)

    def set_options(self, key, value):
        self.options[key] = value

    def get_global_options(self):
        return self.get_options(OptionsType.REQUEST)

    def get_target_options(self):
        return self.get_options(OptionsType.TARGET)

    def get_ansible_options(self):
        return self.get_options(OptionsType.ANSIBLE)
