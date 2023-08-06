from dataclasses import dataclass
from typing import Optional

from .druid_types import DruidNativeType


@dataclass
class Lookup:
    pass


@dataclass
class Map(Lookup):
    map: dict[DruidNativeType, DruidNativeType]
    injective: Optional[bool] = None

    def __post_init__(self):
        self.type = 'map'
