import functools
import logging
from typing import Tuple, Dict, Any, Callable

import pandas as pd
from requests import Response

from algoralabs.common.errors import ApiError

logger = logging.getLogger(__name__)


def _process_response(
        response: Response,
        processor: Callable[[Response], Any],
        transformer: Callable[[Any], Any]
):
    if response.status_code != 200 | response.status_code != 201:
        error = ApiError(
            f"Request to {response.url} failed with status code {response.status_code}: {response.text}"
        )
        logger.error(error)
        raise error

    data = processor(response)
    return transformer(data)


def data_request(
        request: Callable = None,
        *,
        processor: Callable[[Response], Any] = lambda response: response.json(),
        transformer: Callable[[Any], Any] = lambda data: pd.DataFrame(data)
) -> Callable:
    """
    """
    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args: Tuple, **kwargs: Dict[str, Any]) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                The output of the wrapped function
            """
            response: Response = f(*args, **kwargs)
            return _process_response(response, processor, transformer)

        return wrap

    if request is None:
        return decorator
    return decorator(request)


def async_data_request(
        request: Callable = None,
        *,
        processor: Callable[[Response], Any] = lambda response: response.json(),
        transformer: Callable[[Any], Any] = lambda data: pd.DataFrame(data)
):
    """
    """
    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        async def wrap(*args: Tuple, **kwargs: Dict[str, Any]) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                The output of the wrapped function
            """
            response: Response = await f(*args, **kwargs)
            return _process_response(response, processor, transformer)

        return wrap

    if request is None:
        return decorator
    return decorator(request)
