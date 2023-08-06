from dataclasses import dataclass
from typing import Optional

from .filters import Filter
from .dimension_specs import Dimension


@dataclass
class Aggregator:
    pass


@dataclass
class Count(Aggregator):
    name: str

    def __post_init__(self):
        self.type = 'count'


@dataclass
class LongSum(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'longSum'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleSum(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleSum'
        if self.name is None:
            self.name = self.field_name


@dataclass
class FloatSum(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'floatSum'
        if self.name is None:
            self.name = self.field_name


@dataclass
class LongMin(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'longMin'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleMin(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleMin'
        if self.name is None:
            self.name = self.field_name


@dataclass
class FloatMin(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'floatMin'
        if self.name is None:
            self.name = self.field_name


@dataclass
class LongMax(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'longMax'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleMax(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleMax'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleMean(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleMean'
        if self.name is None:
            self.name = self.field_name


@dataclass
class FloatMax(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'floatMax'
        if self.name is None:
            self.name = self.field_name


@dataclass
class LongFirst(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'longFirst'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleFirst(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleFirst'
        if self.name is None:
            self.name = self.field_name


@dataclass
class FloatFirst(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'floatFirst'
        if self.name is None:
            self.name = self.field_name


@dataclass
class StringFirst(Aggregator):
    field_name: str
    name: Optional[str] = None
    max_string_bytes: Optional[int] = None

    def __post_init__(self):
        self.type = 'stringFirst'
        if self.name is None:
            self.name = self.field_name


@dataclass
class LongLast(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'longLast'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleLast(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleLast'
        if self.name is None:
            self.name = self.field_name


@dataclass
class FloatLast(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'floatLast'
        if self.name is None:
            self.name = self.field_name


@dataclass
class StringLast(Aggregator):
    field_name: str
    name: Optional[str] = None
    max_string_bytes: Optional[int] = None

    def __post_init__(self):
        self.type = 'stringLast'
        if self.name is None:
            self.name = self.field_name


@dataclass
class LongAny(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'longAny'
        if self.name is None:
            self.name = self.field_name


@dataclass
class DoubleAny(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'doubleAny'
        if self.name is None:
            self.name = self.field_name


@dataclass
class FloatAny(Aggregator):
    field_name: str
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'floatAny'
        if self.name is None:
            self.name = self.field_name


@dataclass
class StringAny(Aggregator):
    field_name: str
    name: Optional[str] = None
    max_string_bytes: Optional[int] = None

    def __post_init__(self):
        self.type = 'stringAny'
        if self.name is None:
            self.name = self.field_name


@dataclass
class Javascript(Aggregator):
    name: str
    field_names: list[str]
    fn_aggregate: str
    fn_combine: str
    fn_reset: str

    def __post_init__(self):
        self.type = 'javascript'


@dataclass
class Filtered(Aggregator):
    filter: Filter
    aggregator: Aggregator

    def __post_init__(self):
        self.type = 'filtered'


@dataclass
class Grouping(Aggregator):
    name: str
    grouping: list[str]

    def __post_init__(self):
        self.type = 'grouping'


@dataclass
class Cardinality(Aggregator):
    name: str
    fields: list[Dimension]
    by_row: Optional[bool] = None
    round: Optional[bool] = None

    def __post_init__(self):
        self.type = 'cardinality'


@dataclass
class HyperUnique(Aggregator):
    field_name: str
    name: Optional[str] = None
    is_input_hyper_unique: Optional[bool] = None
    round: Optional[bool] = None

    def __post_init__(self):
        self.type = 'hyperUnique'
        if self.name is None:
            self.name = self.field_name
