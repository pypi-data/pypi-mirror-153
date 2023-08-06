from dataclasses import dataclass
from typing import Optional, Union

from .druid_types import DruidNativeType
from .extraction_functions import ExtractionFunction
from . import lookups


@dataclass
class DimensionSpec:
    pass


Dimension = Union[DimensionSpec, str]


@dataclass
class Default(DimensionSpec):
    dimension: str
    output_name: str
    output_type: Optional[str] = None

    def __post_init__(self):
        self.type = 'default'


@dataclass
class Extraction(DimensionSpec):
    dimension: str
    output_name: str
    extraction_fn: ExtractionFunction
    output_type: Optional[str] = None

    def __post_init__(self):
        self.type = 'extraction'


@dataclass
class ListFiltered(DimensionSpec):
    delegate: Dimension
    values: list[str]
    is_whitelist: Optional[bool] = None

    def __post_init__(self):
        self.type = 'listFiltered'


@dataclass
class RegexFiltered(DimensionSpec):
    delegate: Dimension
    pattern: str

    def __post_init__(self):
        self.type = 'regexFiltered'


@dataclass
class PrefixFiltered(DimensionSpec):
    delegate: Dimension
    prefix: str

    def __post_init__(self):
        self.type = 'prefixFiltered'


@dataclass
class Lookup(DimensionSpec):
    dimension: str
    output_name: str
    retain_missing_value: Optional[bool] = None
    replace_missing_value_with: Optional[DruidNativeType] = None
    lookup: Optional[lookups.Lookup] = None
    optimize: Optional[bool] = None
    name: Optional[str] = None

    def __post_init__(self):
        self.type = 'lookup'
