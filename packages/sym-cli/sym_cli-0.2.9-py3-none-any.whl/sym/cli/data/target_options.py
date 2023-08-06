from dataclasses import dataclass, field


@dataclass
class TargetOptions:
    host: str = field(default="")
    port: int = field(default=0)
