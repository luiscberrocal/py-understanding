from typing import Optional

from pydantic import BaseModel

from .enums import FieldType


class FieldInfo(BaseModel):
    name: str
    field_type: FieldType
    factory_entry = Optional[str]


class CharFieldInfo(FieldInfo):
    field_type = FieldType.CHAR_FIELD
    max_length: int


class ModelInfo(BaseModel):
    name: str


if __name__ == '__main__':
    pass
