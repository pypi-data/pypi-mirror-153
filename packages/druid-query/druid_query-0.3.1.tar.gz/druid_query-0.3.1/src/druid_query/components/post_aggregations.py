from dataclasses import dataclass
from typing import Optional

from .druid_types import DruidNativeType


@dataclass
class PostAggregator:
    pass


@dataclass
class Arithmetic(PostAggregator):
    name: str
    fn: str
    fields: list[PostAggregator]
    ordering: Optional[str] = None

    def __post_init__(self):
        self.type = 'arithmetic'


@dataclass
class FieldAccess(PostAggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'fieldAccess'
        if self.name is None:
            self.name = self.field_name

@dataclass
class FinalizingFieldAccess(PostAggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'finalizingFieldAccess'
        if self.name is None:
            self.name = self.field_name


@dataclass
class Constant(PostAggregator):
    name: str
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'constant'


@dataclass
class LongGreatest(PostAggregator):
    name: str
    fields: list[PostAggregator]

    def __post_init__(self):
        self.type = 'longGreatest'


@dataclass
class DoubleGreatest(PostAggregator):
    name: str
    fields: list[PostAggregator]

    def __post_init__(self):
        self.type = 'doubleGreatest'


@dataclass
class LongLeast(PostAggregator):
    name: str
    fields: list[PostAggregator]

    def __post_init__(self):
        self.type = 'longLeast'


@dataclass
class DoubleLeast(PostAggregator):
    name: str
    fields: list[PostAggregator]

    def __post_init__(self):
        self.type = 'doubleLeast'


@dataclass
class Javascript(PostAggregator):
    name: str
    field_names: list[str]
    function: str

    def __post_init__(self):
        self.type = 'javascript'


@dataclass
class HyperUniqueCardinality(PostAggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'hyperUniqueCardinality'
        if self.name is None:
            self.name = self.field_name
