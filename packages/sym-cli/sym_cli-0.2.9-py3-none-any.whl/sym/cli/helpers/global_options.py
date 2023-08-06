from dataclasses import dataclass, field
from typing import Dict, Optional, Type

from sym.shared.cli.data.global_options_base import GlobalOptionsBase

from ..saml_clients.chooser import choose_saml_client
from ..saml_clients.saml_client import SAMLClient


@dataclass
class GlobalOptions(GlobalOptionsBase):
    saml_client_type: Type[SAMLClient] = field(
        default_factory=lambda: choose_saml_client("auto", none_ok=True)
    )
    saml_clients: Dict[str, SAMLClient] = field(default_factory=dict)
    session_length: Optional[int] = None
    aws_region: Optional[str] = None
    disable_caches: bool = False

    def to_dict(self):
        return {
            **super().to_dict(),
            "saml_client": str(self.saml_client_type),
            "session_length": str(self.session_length),
            "aws_region": str(self.aws_region),
            "disable_caches": self.disable_caches,
        }
