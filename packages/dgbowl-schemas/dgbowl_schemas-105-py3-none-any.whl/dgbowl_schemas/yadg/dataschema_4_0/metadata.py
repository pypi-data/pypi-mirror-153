from pydantic import BaseModel, Extra, Field
from typing import Literal


class Metadata(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    version: Literal["4.0", "4.0.0", "4.0.1"] = Field(alias="schema_version")
    provenance: str
    timezone: str = "localtime"
