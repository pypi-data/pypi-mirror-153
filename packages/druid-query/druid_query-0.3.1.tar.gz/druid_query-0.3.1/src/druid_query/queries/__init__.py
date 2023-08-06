from dataclasses import dataclass
from typing import Optional

from ..components import data_sources
from ..components.dimension_specs import Dimension
from ..components.granularities import Granularity
from ..components.virtual_columns import VirtualColumn
from ..components.context import Context
from ..components.intervals import Interval
from ..components.filters import Filter
from ..components.aggregations import Aggregator
from ..components.post_aggregations import PostAggregator
from ..components.topn_metric_specs import TopNMetricSpec
from ..components.limit_specs import LimitSpec
from ..components.having_specs import HavingSpec
from ..components.search_query_specs import SearchQuerySpec
from ..components.to_include import ToInclude
from ..components.druid_types import DruidSqlType

__all__ = [
    'Timeseries', 'TopN', 'GroupBy', 'Scan', 'Search', 'TimeBoundary',
    'SegmentMetadata', 'DatasourceMetadata', 'Sql'
]


class Query:
    pass


class NativeQuery(Query):
    pass


@dataclass
class Timeseries(NativeQuery):
    data_source: data_sources.Datasource
    intervals: list[Interval]
    granularity: Granularity
    descending: Optional[bool] = None
    filter: Optional[Filter] = None
    aggregations: Optional[list[Aggregator]] = None
    post_aggregations: Optional[list[PostAggregator]] = None
    limit: Optional[int] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'timeseries'


@dataclass
class TopN(NativeQuery):
    data_source: data_sources.Datasource
    intervals: list[Interval]
    granularity: Granularity
    dimension: Dimension
    threshold: int
    metric: TopNMetricSpec
    filter: Optional[Filter] = None
    aggregations: Optional[list[Aggregator]] = None
    post_aggregations: Optional[list[PostAggregator]] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'topN'


@dataclass
class GroupBy(NativeQuery):
    data_source: data_sources.Datasource
    intervals: list[Interval]
    granularity: Granularity
    dimensions: list[Dimension]
    limit_spec: Optional[LimitSpec] = None
    having: Optional[HavingSpec] = None
    filter: Optional[Filter] = None
    aggregations: Optional[list[Aggregator]] = None
    post_aggregations: Optional[list[PostAggregator]] = None
    subtotals_spec: Optional[list[list[str]]] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'groupBy'


@dataclass
class Scan(NativeQuery):
    data_source: data_sources.Datasource
    intervals: list[Interval]
    result_format: Optional[str] = None
    filter: Optional[Filter] = None
    columns: Optional[list[str]] = None
    batch_size: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order: Optional[str] = None
    legacy: Optional[bool] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'scan'


@dataclass
class Search(NativeQuery):
    data_source: data_sources.Datasource
    intervals: list[Interval]
    query: SearchQuerySpec
    granularity: Optional[Granularity] = None
    filter: Optional[Filter] = None
    limit: Optional[int] = None
    search_dimensions: Optional[list[str]] = None
    sort: Optional[str] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'search'


@dataclass
class TimeBoundary(NativeQuery):
    data_source: data_sources.Datasource
    bound: Optional[str] = None
    filter: Optional[Filter] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'timeBoundary'


@dataclass
class SegmentMetadata(NativeQuery):
    data_source: data_sources.Datasource
    intervals: list[Interval]
    to_include: Optional[ToInclude] = None
    merge: Optional[bool] = None
    analysis_types: Optional[list[str]] = None
    lenient_aggregator_merge: Optional[bool] = None
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'segmentMetadata'


@dataclass
class DatasourceMetadata(NativeQuery):
    data_source: data_sources.Datasource
    virtual_columns: Optional[list[VirtualColumn]] = None
    context: Optional[Context] = None

    def __post_init__(self):
        self.query_type = 'datasourceMetadata'


@dataclass
class Sql(Query):
    query: str
    result_format: Optional[str] = 'object'
    header: Optional[bool] = None
    parameters: Optional[list[DruidSqlType]] = None
    context: Optional[Context] = None
