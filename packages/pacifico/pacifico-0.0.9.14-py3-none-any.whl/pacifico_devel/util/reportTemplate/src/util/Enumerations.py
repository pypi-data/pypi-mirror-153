from enum import Enum, auto


class PlotKind(Enum):
    LINE_PLOT = auto()
    BAR_PLOT = auto()
    TABLE_PLOT = auto()


class Backend(Enum):
    BOKEH = auto()
    ALTAIR = auto()
