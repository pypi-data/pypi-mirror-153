from pydantic import BaseModel, Extra, Field


class Method(BaseModel, extra=Extra.allow):
    device: str
    technique: str
