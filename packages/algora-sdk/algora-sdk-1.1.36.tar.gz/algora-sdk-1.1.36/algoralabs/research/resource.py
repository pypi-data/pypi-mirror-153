from typing import Dict, Any

from algoralabs.common.requests import __get_request, __delete_request
from algoralabs.decorators.data import data_request


@data_request(
    transformer=lambda data: data,
    processor=lambda response: response.content
)
def get_resource(id: str) -> Dict[str, Any]:
    endpoint = f"config/research/resource/{id}/code"
    return __get_request(endpoint)


def delete_resource(id: str) -> None:
    endpoint = f"config/research/resource/{id}"
    return __delete_request(endpoint)
