from dataclasses import dataclass
from typing import Optional

from .search_query_specs import SearchQuerySpec
from .granularities import Granularity
from .druid_types import DruidNativeType
from . import lookups


@dataclass
class ExtractionFunction:
    pass


@dataclass
class Regex(ExtractionFunction):
    expr: str
    index: Optional[int] = None
    replace_missing_value: Optional[bool] = None
    replace_missing_value_with: Optional[DruidNativeType] = None

    def __post_init__(self):
        self.type = 'regex'


@dataclass
class Partial(ExtractionFunction):
    expr: str

    def __post_init__(self):
        self.type = 'partial'


@dataclass
class SearchQuery(ExtractionFunction):
    query: SearchQuerySpec

    def __post_init__(self):
        self.type = 'searchQuery'


@dataclass
class Substring(ExtractionFunction):
    index: int
    length: Optional[int] = None

    def __post_init__(self):
        self.type = 'substring'


@dataclass
class Strlen(ExtractionFunction):
    def __post_init__(self):
        self.type = 'strlen'


@dataclass
class TimeFormat(ExtractionFunction):
    format: Optional[str] = None
    time_zone: Optional[str] = None
    locale: Optional[str] = None
    granularity: Optional[Granularity] = None
    as_millis: Optional[bool] = None

    def __post_init__(self):
        self.type = 'timeFormat'


@dataclass
class Time(ExtractionFunction):
    time_format: str
    result_format: str
    joda: bool

    def __post_init__(self):
        self.type = 'time'


@dataclass
class Javascript(ExtractionFunction):
    function: str
    injective: Optional[bool] = None

    def __post_init__(self):
        self.type = 'javascript'


@dataclass
class RegisteredLookup(ExtractionFunction):
    lookup: str
    retain_missing_value: Optional[bool] = None
    replace_missing_value_with: Optional[DruidNativeType] = None
    injective: Optional[bool] = None
    optimize: Optional[bool] = None

    def __post_init__(self):
        self.type = 'registeredLookup'


@dataclass
class Lookup(ExtractionFunction):
    lookup: lookups.Lookup
    retain_missing_value: Optional[bool] = None
    replace_missing_value_with: Optional[DruidNativeType] = None
    injective: Optional[bool] = None
    optiomize: Optional[bool] = None

    def __post_init__(self):
        self.type = 'lookup'


@dataclass
class Cascade(ExtractionFunction):
    extraction_fns: list[ExtractionFunction]

    def __post_init__(self):
        self.type = 'cascade'


@dataclass
class StringFormat(ExtractionFunction):
    format: str
    null_handling: Optional[str] = None

    def __post_init__(self):
        self.type = 'stringFormat'


@dataclass
class Upper(ExtractionFunction):
    locale: Optional[str] = None

    def __post_init__(self):
        self.type = 'upper'


@dataclass
class Lower(ExtractionFunction):
    locale: Optional[str] = None

    def __post_init__(self):
        self.type = 'lower'


@dataclass
class Bucket(ExtractionFunction):
    size: Optional[int] = None
    offset: Optional[int] = None

    def __post_init__(self):
        self.type = 'bucket'
