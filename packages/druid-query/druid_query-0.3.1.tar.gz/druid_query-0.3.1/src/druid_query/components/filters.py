from dataclasses import dataclass
from typing import Optional

from .dimension_specs import Dimension
from .extraction_functions import ExtractionFunction
from .search_query_specs import SearchQuerySpec
from . import intervals


@dataclass
class Filter:
    pass


@dataclass
class Selector(Filter):
    dimension: Dimension
    value: str
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'selector'


@dataclass
class ColumnComparison(Filter):
    dimensions: list[Dimension]

    def __post_init__(self):
        self.type = 'columnComparison'


@dataclass
class Regex(Filter):
    dimension: Dimension
    pattern: str
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'regex'


@dataclass
class And(Filter):
    fields: list[Filter]

    def __post_init__(self):
        self.type = 'and'


@dataclass
class Or(Filter):
    fields: list[Filter]

    def __post_init__(self):
        self.type = 'or'


@dataclass
class Not(Filter):
    field: Filter

    def __post_init__(self):
        self.type = 'not'


@dataclass
class Javascript(Filter):
    dimension: Dimension
    function: str
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'javascript'


@dataclass
class Extraction(Filter):
    dimension: Dimension
    value: str
    extraction_fn: ExtractionFunction

    def __post_init__(self):
        self.type = 'extraction'


@dataclass
class Search(Filter):
    dimension: Dimension
    query: SearchQuerySpec
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'search'


@dataclass
class In(Filter):
    dimension: Dimension
    values: list[str]

    def __post_init__(self):
        self.type = 'in'


@dataclass
class Like(Filter):
    dimension: str
    pattern: str
    escape: Optional[str] = None
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'like'


@dataclass
class Bound(Filter):
    dimension: str
    lower: Optional[str] = None
    upper: Optional[str] = None
    lower_strict: Optional[bool] = None
    upper_strict: Optional[bool] = None
    orderring: Optional[str] = None
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'bound'


@dataclass
class Interval(Filter):
    dimension: str
    intervals: list[intervals.Interval]
    extraction_fn: Optional[ExtractionFunction] = None

    def __post_init__(self):
        self.type = 'interval'


@dataclass
class Expression(Filter):
    expression: str

    def __post_init__(self):
        self.type = 'expression'


@dataclass
class TrueF(Filter):
    def __post_init__(self):
        self.type = 'true'


@dataclass
class SpatialBound:
    pass


@dataclass
class Rectangular(SpatialBound):
    min_coords: list[float]
    max_coords: list[float]

    def __post_init__(self):
        self.type = 'rectangular'


@dataclass
class Radius(SpatialBound):
    coords: list[float]
    radius: float

    def __post_init__(self):
        self.type = 'radius'


@dataclass
class Polygon(SpatialBound):
    abscissa: list[float]
    ordinate: list[float]

    def __post_init__(self):
        self.type = 'polygon'


@dataclass
class Spatial(Filter):
    dimension: str
    bound: SpatialBound

    def __post_init__(self):
        self.type = 'spatial'
