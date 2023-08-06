from pydantic import BaseModel, Extra
from typing import Literal, Optional, Union


class ExternalDateFile(BaseModel, extra=Extra.forbid):
    class Content(BaseModel, extra=Extra.forbid):
        path: str
        type: str
        match: Optional[str]

    file: Content


class ExternalDateFilename(BaseModel, extra=Extra.forbid):
    class Content(BaseModel, extra=Extra.forbid):
        format: str
        len: int

    filename: Content


class ExternalDateISOString(BaseModel, extra=Extra.forbid):
    isostring: str


class ExternalDateUTSOffset(BaseModel, extra=Extra.forbid):
    utsoffset: float


class ExternalDate(BaseModel, extra=Extra.forbid):
    using: Union[
        ExternalDateFile,
        ExternalDateFilename,
        ExternalDateISOString,
        ExternalDateUTSOffset,
    ]
    mode: Literal["add", "replace"] = "add"
