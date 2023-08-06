from pydantic import BaseModel, Extra, Field
from typing import Literal, Sequence, Optional, Tuple, Any


class SeriesIndex(BaseModel, extra=Extra.forbid):
    from_zero: bool = True
    to_units: Optional[str]


class Series(BaseModel, extra=Extra.allow):
    y: str
    x: Optional[str]
    kind: Literal["scatter", "line", "errorbar"] = "scatter"
    index: Optional[SeriesIndex] = SeriesIndex()


class AxArgs(BaseModel, extra=Extra.allow):
    cols: Optional[Tuple[int, int]]
    rows: Optional[Tuple[int, int]]
    series: Sequence[Series]
    methods: Optional[dict[str, Any]]
    legend: bool = False


class PlotSave(BaseModel, extra=Extra.allow, allow_population_by_field_name=True):
    as_: str = Field(alias="as")
    tight_layout: Optional[dict[str, Any]]


class Plot(BaseModel, extra=Extra.forbid):
    table: str
    ax_args: Sequence[AxArgs]
    fig_args: Optional[dict[str, Any]]
    style: Optional[dict[str, Any]]
    nrows: int = 1
    ncols: int = 1
    save: Optional[PlotSave]
