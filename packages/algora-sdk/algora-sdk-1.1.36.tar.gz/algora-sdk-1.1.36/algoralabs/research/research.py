from typing import Dict, Any

from algoralabs.common.requests import __get_request
from algoralabs.decorators.data import data_request


@data_request(transformer=lambda data: data)
def get_research(id: str) -> Dict[str, Any]:
    endpoint = f"config/research/research/{id}"
    return __get_request(endpoint)
