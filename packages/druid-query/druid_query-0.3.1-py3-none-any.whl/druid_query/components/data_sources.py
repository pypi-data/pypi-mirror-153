from dataclasses import dataclass
from typing import Any
import typing

from .druid_types import DruidNativeType


@dataclass
class DataSource:
    pass


Datasource = typing.Union[DataSource, str]


@dataclass
class Table(DataSource):
    name: str

    def __post_init__(self):
        self.type = 'table'


@dataclass
class Lookup(DataSource):
    lookup: str

    def __post_init__(self):
        self.type = 'lookup'


@dataclass
class Union(DataSource):
    data_sources: list[str]

    def __post_init__(self):
        self.type = 'union'


@dataclass
class Inline(DataSource):
    column_names: list[str]
    rows: list[list[DruidNativeType]]

    def __post_init__(self):
        self.type = 'inline'


@dataclass
class Query(DataSource):
    query: Any

    def __post_init__(self):
        from .. import queries
        if not isinstance(self.query, queries.NativeQuery):
            raise TypeError('query must be a native query')
        self.type = 'query'


@dataclass
class Join(DataSource):
    left: Datasource
    right: Datasource
    right_prefix: str
    condition: str
    join_type: str

    def __post_init__(self):
        self.type = 'join'
