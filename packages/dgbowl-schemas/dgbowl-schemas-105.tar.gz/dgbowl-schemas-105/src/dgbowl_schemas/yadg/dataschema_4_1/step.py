from pydantic import BaseModel, Extra, Field
from typing import Optional, Literal, Mapping, Any, Union
from .externaldate import ExternalDate
from .input import Input
from .parameters import Tol, Timestamps, Timestamp


class Dummy(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.allow):
        pass

    parser: Literal["dummy"]
    input: Input
    parameters: Optional[Params]
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class BasicCSV(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        sep: str = ","
        sigma: Optional[Mapping[str, Tol]]
        calfile: Optional[str]
        timestamp: Optional[Timestamps]
        convert: Optional[Any]
        units: Optional[Mapping[str, str]]

    parser: Literal["basiccsv"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class MeasCSV(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        timestamp: Timestamps = Field(
            Timestamp(timestamp={"index": 0, "format": "%Y-%m-%d-%H-%M-%S"})
        )
        calfile: Optional[str]
        convert: Optional[Any]

    parser: Literal["meascsv"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class FlowData(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["drycal.csv", "drycal.rtf", "drycal.txt"] = "drycal.csv"
        convert: Optional[Any]
        calfile: Optional[str]

    parser: Literal["flowdata"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class ElectroChem(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["eclab.mpt", "eclab.mpr", "tomato.json"] = "eclab.mpr"

    class Input(Input):
        encoding: str = "windows-1252"

    parser: Literal["electrochem"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class ChromTrace(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal[
            "ezchrom.asc",
            "fusion.json",
            "fusion.zip",
            "agilent.ch",
            "agilent.dx",
            "agilent.csv",
        ] = "ezchrom.asc"
        calfile: Optional[str]
        species: Optional[Any]
        detectors: Optional[Any]

    parser: Literal["chromtrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class MassTrace(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["quadstar.sac"] = "quadstar.sac"

    parser: Literal["masstrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class QFTrace(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["labview.csv"] = "labview.csv"
        method: Literal["naive", "lorentz", "kajfez"] = "kajfez"
        height: float = 1.0
        distance: float = 5000.0
        cutoff: float = 0.4
        threshold: float = 1e-6

    parser: Literal["qftrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class XPSTrace(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["phi.spe"] = "phi.spe"

    parser: Literal["xpstrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


class XRDTrace(BaseModel, extra=Extra.forbid):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal[
            "panalytical.xy", "panalytical.csv", "panalytical.xrdml"
        ] = "panalytical.csv"

    parser: Literal["xrdtrace"]
    input: Input
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]


Steps = Union[
    Dummy,
    BasicCSV,
    MeasCSV,
    FlowData,
    ElectroChem,
    ChromTrace,
    MassTrace,
    QFTrace,
    XPSTrace,
    XRDTrace,
]
