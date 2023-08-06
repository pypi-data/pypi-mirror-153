from pydantic import BaseModel, Extra, Field
from typing import Optional, Sequence
import os


class Input(BaseModel, extra=Extra.forbid, allow_population_by_field_name=True):
    files: Sequence[str] = Field(alias="folders")
    prefix: Optional[str]
    suffix: Optional[str]
    contains: Optional[str]
    exclude: Optional[str]
    encoding: str = "UTF-8"

    def paths(self) -> list[str]:
        ret = []
        for item in sorted(self.files):
            if os.path.isdir(item):
                paths = [os.path.join(item, fn) for fn in sorted(os.listdir(item))]
            else:
                paths = [item]
            for path in paths:
                tail = os.path.basename(path)
                inc = True
                if self.prefix is not None and not tail.startswith(self.prefix):
                    inc = False
                if self.suffix is not None and not tail.endswith(self.suffix):
                    inc = False
                if self.contains is not None and self.contains not in tail:
                    inc = False
                if self.exclude is not None and self.exclude in tail:
                    inc = False
                if inc:
                    ret.append(path)
        return ret
