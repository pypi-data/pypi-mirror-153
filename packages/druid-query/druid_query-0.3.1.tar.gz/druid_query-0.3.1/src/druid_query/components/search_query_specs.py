from dataclasses import dataclass

from .druid_types import DruidNativeType


@dataclass
class SearchQuerySpec:
    pass


@dataclass
class InsensitiveContains(SearchQuerySpec):
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'insensitiveContains'


@dataclass
class Fragment(SearchQuerySpec):
    case_sensitive: bool
    values: list[DruidNativeType]

    def __post_init__(self):
        self.type = 'fragment'


@dataclass
class Contains(SearchQuerySpec):
    case_sensitive: bool
    value: DruidNativeType

    def __post_init__(self):
        self.type = 'contains'


@dataclass
class Regex(SearchQuerySpec):
    pattern: str

    def __post_init__(self):
        self.type = 'regex'
