from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from algoralabs.common.enum import FieldType


class DatasetDataType(Enum):
    STOCK = 'STOCK'


class DatasetRequest(BaseModel):
    display_name: str
    logical_name: str
    description: Optional[str]
    data_type: DatasetDataType
    data_query: str
    data_query_type: str
    schema_id: str
    directory_id: str


class DatasetSearchRequest(BaseModel):
    query: str
    data_types: Optional[List[str]]  # TODO make enum


class DatasetSummaryResponse(BaseModel):
    id: str
    display_name: str
    logical_name: str
    description: Optional[str]
    data_type: str  # TODO make enum
    tag: str


class FieldRequest(BaseModel):
    display_name: str
    logical_name: str
    type: FieldType
    width: int
    editable: bool
    hidden: bool
    display_order: int
    tags: List[str]  # TODO make enum
    schema_id: str
    field_group_id: Optional[str]


class FieldGroupRequest(BaseModel):
    display_name: str
    logical_name: str


class SchemaRequest(BaseModel):
    display_name: str
    logical_name: str


class SchemaResponse(BaseModel):
    id: str
    display_name: str
    logical_name: str
