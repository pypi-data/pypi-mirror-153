from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class AnsibleOptions:
    command: Tuple[str, ...]
    control_master: bool
    send_command: bool
    forks: int
    ssm_timeout: int
    ansible_aws_profile: Optional[str] = None
    ansible_sym_resource: Optional[str] = None
