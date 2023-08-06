from enum import Enum
from typing import List, Optional, Union

import pydantic
from fastapi import Form, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status

from algoralabs.common.enum import FieldType


class FieldMetric(BaseModel):
    name: str
    type: FieldType
    length: int
    num_null: int
    num_zero: int
    min: Optional[Union[float, int]]
    max: Optional[Union[float, int]]
    std_dev: Optional[float]


class FieldFill(Enum):
    NULL = 'NULL'
    ZERO = 'ZERO'
    PREVIOUS = 'PREVIOUS'
    NEXT = 'NEXT'


class FieldOverride(BaseModel):
    name: str
    type: Optional[FieldType] = None
    fill: Optional[FieldFill] = None


class TransformOverride(BaseModel):
    fields: List[FieldOverride] = []
    default_fill: FieldFill = FieldFill.PREVIOUS


async def transformer(transform_override: Optional[str] = Form(None)):
    try:
        if transform_override is None:
            return TransformOverride()
        return TransformOverride.parse_raw(transform_override)
    except pydantic.ValidationError as e:
        raise HTTPException(detail=jsonable_encoder(e.errors()), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
