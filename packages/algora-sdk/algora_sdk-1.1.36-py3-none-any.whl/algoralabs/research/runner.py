from algoralabs.common.requests import __put_request
from algoralabs.decorators.data import data_request


@data_request(transformer=lambda data: data)
def get_or_create_runner() -> str:
    endpoint = f"research-service/runner/deployment"
    return __put_request(endpoint)
