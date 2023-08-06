from pydantic import BaseModel, Extra
from typing import Optional, Union

from .timestamp import Timestamp, TimeDate, UTS


class Tol(BaseModel, extra=Extra.forbid):
    atol: Optional[float]
    rtol: Optional[float]


Timestamps = Union[Timestamp, TimeDate, UTS]
