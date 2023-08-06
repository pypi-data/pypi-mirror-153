from dataclasses import dataclass
from typing import Optional


@dataclass
class LimitSpec:
    pass


@dataclass
class OrderByColumnSpec:
    dimension: str
    direction: str
    dimension_order: Optional[str] = None


@dataclass
class Default(LimitSpec):
    limit: Optional[int] = None
    offset: Optional[int] = None
    columns: Optional[list[OrderByColumnSpec]] = None

    def __post_init__(self):
        self.type = 'default'
