from pydantic import BaseModel, Extra, Field


class Sample(BaseModel, extra=Extra.allow):
    name: str
