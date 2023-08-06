from dataclasses import dataclass
from typing import Optional


@dataclass
class VirtualColumn:
    pass


@dataclass
class Expression(VirtualColumn):
    name: str
    expression: str
    output_type: Optional[str] = None

    def __post_init__(self):
        self.type = 'expression'
