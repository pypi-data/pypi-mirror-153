import json
from typing import Dict, List, Any

from algoralabs.data.datasets.models import FieldGroupRequest
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request,async_data_request
from algoralabs.common.requests import (
    __get_request, __put_request, __post_request, __delete_request,
    __async_get_request, __async_put_request, __async_post_request, __async_delete_request
)


def _get_field_group_request_info(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/field-group/{id}"
    }


@data_request(transformer=no_transform)
def get_field_group(id: str) -> Dict[str, Any]:
    request_info = _get_field_group_request_info(id)
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_field_group(id: str) -> Dict[str, Any]:
    request_info = _get_field_group_request_info(id)
    return __get_request(**request_info)


def _get_field_groups_request_info() -> dict:
    return {
        "endpoint": f"config/datasets/field-group"
    }


@data_request(transformer=no_transform)
def get_field_groups() -> List[Dict[str, Any]]:
    request_info = _get_field_groups_request_info()
    return __get_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_get_field_groups() -> List[Dict[str, Any]]:
    request_info = _get_field_groups_request_info()
    return await __async_get_request(**request_info)


def _create_field_group_request_info(request: FieldGroupRequest) -> dict:
    return {
        "endpoint": f"config/datasets/field-group",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def create_field_group(request: FieldGroupRequest) -> Dict[str, Any]:
    request_info = _create_field_group_request_info(request)
    return __put_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_create_field_group(request: FieldGroupRequest) -> Dict[str, Any]:
    request_info = _create_field_group_request_info(request)
    return await __async_put_request(**request_info)


def _update_field_group_request_info(id: str, request: FieldGroupRequest) -> dict:
    return {
        "endpoint": f"config/datasets/field-group/{id}",
        "json": json.loads(request.json())
    }


@data_request(transformer=no_transform)
def update_field_group(id: str, request: FieldGroupRequest) -> Dict[str, Any]:
    request_info = _update_field_group_request_info(id, request)
    return __post_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_update_field_group(id: str, request: FieldGroupRequest) -> Dict[str, Any]:
    request_info = _update_field_group_request_info(id, request)
    return __post_request(**request_info)


def delete_field_group(id: str) -> dict:
    return {
        "endpoint": f"config/datasets/field-group/{id}"
    }


@data_request(transformer=no_transform)
def delete_field_group(id: str) -> None:
    endpoint = f"config/datasets/field-group/{id}"
    return __delete_request(endpoint)


@async_data_request(transformer=no_transform)
async def async_delete_field_group(id: str) -> None:
    endpoint = f"config/datasets/field-group/{id}"
    return await __async_delete_request(endpoint)
