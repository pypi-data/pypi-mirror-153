from enum import Enum

from pydantic import BaseModel


class PermissionType(Enum):
    USER_ID = "USER_ID"
    GROUP = "GROUP"
    ROLE = "ROLE"


class FieldType(Enum):
    BOOLEAN = 'BOOLEAN'
    DOUBLE = 'DOUBLE'
    INTEGER = 'INTEGER'
    TEXT = 'TEXT'
    TIMESTAMP = 'TIMESTAMP'
    DATETIME = 'DATETIME'
    UNKNOWN = 'UNKNOWN'


class PermissionRequest(BaseModel):
    resource_id: str
    permission_type: PermissionType
    permission_id: str
    view: bool
    edit: bool
    delete: bool
    edit_permission: bool


class Field(BaseModel):
    logical_name: str
    type: FieldType
