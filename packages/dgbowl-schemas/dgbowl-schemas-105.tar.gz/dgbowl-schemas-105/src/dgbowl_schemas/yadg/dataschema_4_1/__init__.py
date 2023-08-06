from pydantic import BaseModel, Extra
from typing import Sequence
from .metadata import Metadata
from .step import Steps


class DataSchema(BaseModel, extra=Extra.forbid):
    metadata: Metadata
    steps: Sequence[Steps]
