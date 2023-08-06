from dataclasses import dataclass

from . import filters
from .druid_types import DruidNativeType


@dataclass
class HavingSpec:
    pass


@dataclass
class Filter(HavingSpec):
    filter: filters.Filter

    def __post_init__(self):
        self.type = 'filter'


@dataclass
class EqualTo(HavingSpec):
    aggregation: str
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'equalTo'


@dataclass
class GreaterThan(HavingSpec):
    aggregation: str
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'greaterThan'


@dataclass
class LessThan(HavingSpec):
    aggregation: str
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'lessThan'


@dataclass
class DimSelector(HavingSpec):
    dimension: str
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'dimSelector'


@dataclass
class And(HavingSpec):
    having_specs: list[HavingSpec]

    def __post_init__(self):
        self.type = 'and'


@dataclass
class Or(HavingSpec):
    having_specs: list[HavingSpec]

    def __post_init__(self):
        self.type = 'or'


@dataclass
class Not(HavingSpec):
    having_spec: HavingSpec

    def __post_init__(self):
        self.type = 'not'
