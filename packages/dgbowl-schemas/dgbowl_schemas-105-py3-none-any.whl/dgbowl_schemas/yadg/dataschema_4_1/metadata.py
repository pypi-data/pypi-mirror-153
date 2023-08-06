from pydantic import BaseModel, Extra
from typing import Optional, Mapping, Literal, Any, Union


class Metadata(BaseModel, extra=Extra.forbid):
    class Provenance(BaseModel, extra=Extra.forbid):
        type: str
        metadata: Optional[Mapping[str, Any]]

    provenance: Provenance
    version: Literal["4.1", "4.1.1"]
    timezone: str = "localtime"
