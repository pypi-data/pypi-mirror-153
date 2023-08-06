from pydantic import BaseModel, Field, root_validator
from typing import Optional, Sequence, Any
import logging

logger = logging.getLogger(__name__)


class At(BaseModel, extra="forbid"):
    steps: Sequence[str] = None
    indices: Sequence[int] = None
    timestamps: Sequence[float] = None

    @root_validator(pre=True)
    def check_one_input(cls, values):
        keys = {"step", "steps", "index", "indices", "timestamp"}
        assert len(keys.intersection(set(values))) == 1, (
            "multiple keys provided: " f"{keys.intersection(values)}"
        )
        if "step" in values:
            values["steps"] = [values.pop("step")]
        elif "index" in values:
            values["indices"] = [values.pop("index")]
        return values


class Constant(BaseModel, extra="forbid"):
    value: Any
    as_: str = Field(alias="as")
    units: Optional[str]


class Column(BaseModel, extra="forbid"):
    key: str
    as_: str = Field(alias="as")


class Extract(BaseModel, extra="forbid"):
    into: str
    from_: Optional[str] = Field(alias="from")
    at: Optional[At]
    constants: Optional[Sequence[Constant]]
    columns: Optional[Sequence[Column]]

    @root_validator(pre=True)
    def check_one_input(cls, values):
        keys = {"constants", "columns"}
        if len(keys.intersection(set(values))) == 0:
            logging.info("did not provide any of '%s'", keys)
        return values
