from pydantic import BaseModel, Extra, Field
from typing import Literal


class Save(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    table: str
    as_: str = Field(alias="as")
    type: Literal["pkl", "json", "xlsx", "csv"] = None
    sigma: bool = True
