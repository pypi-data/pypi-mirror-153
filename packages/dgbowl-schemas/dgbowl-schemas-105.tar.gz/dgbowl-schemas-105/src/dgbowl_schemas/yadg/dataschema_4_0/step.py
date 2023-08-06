from pydantic import BaseModel, Extra, Field
from typing import Optional, Literal, Mapping, Any, Union
from .externaldate import ExternalDate
from .input import Input
from .parameters import Tol, Timestamps, Timestamp


class Dummy(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.allow):
        pass

    parser: Literal["dummy"]
    input: Input = Field(alias="import")
    parameters: Optional[Params]
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class BasicCSV(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        sep: str = ","
        sigma: Optional[Mapping[str, Tol]]
        calfile: Optional[str]
        timestamp: Optional[Timestamps]
        convert: Optional[Any]
        units: Optional[Mapping[str, str]]

    parser: Literal["basiccsv"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class MeasCSV(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        timestamp: Timestamps = Field(
            Timestamp(timestamp={"index": 0, "format": "%Y-%m-%d-%H-%M-%S"})
        )
        calfile: Optional[str]
        convert: Optional[Any]

    parser: Literal["meascsv"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class FlowData(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["drycal", "drycal.csv", "drycal.rtf", "drycal.txt"] = "drycal"
        convert: Optional[Any]
        calfile: Optional[str]

    parser: Literal["flowdata"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class ElectroChem(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["eclab.mpt", "eclab.mpr"] = "eclab.mpr"

    class ECInput(Input):
        encoding: str = "windows-1252"

    parser: Literal["electrochem"]
    input: ECInput = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class ChromTrace(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal[
            "ezchrom.asc",
            "fusion.json",
            "fusion.zip",
            "agilent.ch",
            "agilent.dx",
            "agilent.csv",
        ] = Field("ezchrom.asc", alias="tracetype")
        calfile: Optional[str]
        species: Optional[Any]
        detectors: Optional[Any]

    parser: Literal["chromtrace"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class MassTrace(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["quadstar.sac"] = Field("quadstar.sac", alias="tracetype")

    parser: Literal["masstrace"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class QFTrace(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["labview.csv"] = Field("labview.csv", alias="tracetype")
        method: Literal["naive", "lorentz", "kajfez"] = "kajfez"
        height: float = 1.0
        distance: float = 5000.0
        cutoff: float = 0.4
        threshold: float = 1e-6

    parser: Literal["qftrace"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


class XPSTrace(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    class Params(BaseModel, extra=Extra.forbid):
        filetype: Literal["phi.spe"] = Field("phi.spe", alias="tracetype")

    parser: Literal["xpstrace"]
    input: Input = Field(alias="import")
    parameters: Params = Field(default_factory=Params)
    tag: Optional[str]
    externaldate: Optional[ExternalDate]
    export: Optional[str]


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
]
