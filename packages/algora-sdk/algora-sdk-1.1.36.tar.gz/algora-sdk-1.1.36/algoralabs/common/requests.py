from typing import Optional
from requests import Response
import aiohttp
import requests

from algoralabs.common.config import EnvironmentConfig
from algoralabs.decorators.authorization import authenticated_request


config = EnvironmentConfig()


async def _build_response_obj(aio_response) -> Response:
    content = await aio_response.content.read()

    response = Response()
    response._content = content
    response.url = str(aio_response.url)
    response.status_code = aio_response.status
    headers = {row[0]: row[1] for row in aio_response.headers.items()}
    response.headers = headers
    return response


@authenticated_request
def __get_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    return requests.get(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
async def __async_get_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"{config.get_url(url_key)}/{endpoint}",
            headers=headers or {},
            params=params,
            timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result


@authenticated_request
def __put_request(
        endpoint: str,
        url_key: str = "algora",
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    return requests.put(
        url=f"{config.get_url(url_key)}/{endpoint}",
        data=data,
        json=json,
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
async def __async_put_request(
        endpoint: str,
        url_key: str = "algora",
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    async with aiohttp.ClientSession() as session:
        async with session.put(
            url=f"{config.get_url(url_key)}/{endpoint}",
            data=data,
            json=json,
            headers=headers or {},
            params=params,
            timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result


@authenticated_request
def __post_request(
        endpoint: str,
        url_key: str = "algora",
        files=None,
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    return requests.post(
        url=f"{config.get_url(url_key)}/{endpoint}",
        files=files,
        data=data,
        json=json,
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
async def __async_post_request(
        endpoint: str,
        url_key: str = "algora",
        files=None,
        data=None,
        json=None,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    data = data if data is None else data.update({"files": files})
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{config.get_url(url_key)}/{endpoint}",
            data=data,
            json=json,
            headers=headers or {},
            params=params,
            timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result


@authenticated_request
def __delete_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    return requests.delete(
        url=f"{config.get_url(url_key)}/{endpoint}",
        headers=headers or {},
        params=params,
        timeout=timeout
    )


@authenticated_request
async def __async_delete_request(
        endpoint: str,
        url_key: str = "algora",
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        timeout: int = 30
) -> Response:
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            url=f"{config.get_url(url_key)}/{endpoint}",
            headers=headers or {},
            params=params,
            timeout=timeout
        ) as response:
            result = await _build_response_obj(response)

    return result
