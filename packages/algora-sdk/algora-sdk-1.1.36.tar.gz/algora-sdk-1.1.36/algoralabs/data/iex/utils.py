from typing import Union, List, Dict, Any
from pandas import DataFrame

from algoralabs.common.requests import __get_request, __async_get_request


def __build_url(extension: str) -> str:
    return f"data/datasets/query/iex/{extension}"


def __base_request(extension: str, **kwargs):
    """
    Base GET request for IEX

    :param extension: URI extension
    :param kwargs: request query params
    :return: response
    """
    return __get_request(endpoint=__build_url(extension), params=kwargs)


async def __async_base_request(extension: str, **kwargs):
    """
    Base GET request for IEX

    :param extension: URI extension
    :param kwargs: request query params
    :return: response
    """
    return await __async_get_request(endpoint=__build_url(extension), params=kwargs)


def transform_one_or_many(
        data: Union[List[Dict[str, Any]], Dict[str, List[Dict[str, Any]]]],
        key: str
) -> Union[DataFrame, Dict[str, DataFrame]]:
    if isinstance(data, dict):
        for s in data:
            data[s] = DataFrame(data[s][key])
        return data

    return DataFrame(data)
