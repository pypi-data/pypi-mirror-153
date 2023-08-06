from dataclasses import dataclass
from typing import Optional


@dataclass
class TopNMetricSpec:
    pass


@dataclass
class Numeric(TopNMetricSpec):
    metric: str

    def __post_init__(self):
        self.type = 'numeric'


@dataclass
class Dimension(TopNMetricSpec):
    ordering: Optional[str] = None
    previous_stop: Optional[str] = None

    def __post_init__(self):
        self.type = 'dimension'


@dataclass
class Inverted(TopNMetricSpec):
    metric: TopNMetricSpec

    def __post_init__(self):
        self.type = 'inverted'
