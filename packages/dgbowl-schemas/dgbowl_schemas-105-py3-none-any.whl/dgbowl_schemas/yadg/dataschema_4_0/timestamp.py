from pydantic import BaseModel, Extra
from typing import Optional


class TimestampSpec(BaseModel, extra=Extra.forbid):
    index: Optional[int]
    format: Optional[str]


class Timestamp(BaseModel, extra=Extra.forbid):
    timestamp: TimestampSpec


class UTS(BaseModel, extra=Extra.forbid):
    uts: TimestampSpec


class TimeDate(BaseModel, extra=Extra.forbid):
    date: Optional[TimestampSpec]
    time: Optional[TimestampSpec]
