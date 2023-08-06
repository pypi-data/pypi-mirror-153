from dataclasses import dataclass


@dataclass
class ToInclude:
    pass


@dataclass
class All(ToInclude):
    def __post_init__(self):
        self.type = 'all'


@dataclass
class Nothing(ToInclude):
    def __post_init__(self):
        self.type = 'nothing'


@dataclass
class List(ToInclude):
    columns: list[str]

    def __post_init__(self):
        self.type = 'list'
