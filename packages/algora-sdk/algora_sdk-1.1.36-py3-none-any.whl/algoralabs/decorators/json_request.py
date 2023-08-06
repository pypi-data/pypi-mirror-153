import dataclasses
from dataclasses import dataclass, field
from functools import partialmethod
from typing import Callable, Any
from flask import request


from algoralabs.decorators.__util import __dataclass_to_json_str, __get_input, __initialize_data_class
from algoralabs.common.errors import InvalidRequest


def __initializer(data_cls: dataclasses.dataclass, default_override: Callable[[], Any] = None, *args, **kwargs) -> None:
    """
    The __init__ method for the json_request

    Parameters:
        data_cls: The json_request class
        default_callable: Callable to override the input generator function
        *args: The arg tuple passed to the method
        **kwargs: The keyword dictionary passed to the method
    """
    default_callable = default_override or (lambda: request.json)
    inp: dict = __get_input(default_callable, **kwargs)
    __initialize_data_class(data_cls, inp, InvalidRequest)


def optional(default_value=None) -> field:
    """
    A method that generates the optional field representation for json_request objects

    Parameters:
        default_value: The default value for the optioanl field

    Returns:
        The field with the needed stuff to represent an optional field
    """
    return field(default=default_value)


def json_request(
        _cls: object = None,
        *,
        input_generator: Callable[[], dict] = None,
        **data_class_args
):
    """
        A decorator used to turn classes (modeled like dataclasses) to json_request objects

    Parameters:
        _cls: The class being decorated
        input_generator: Callable to override the input generator function
        **data_class_args: keyword args passed to the dataclass constructor

    Returns:
        The updated class with the json_request methods
    """
    def wrap(cls):
        setattr(cls, "__init__", partialmethod(__initializer, default_override=input_generator))
        setattr(cls, "__str__", partialmethod(__dataclass_to_json_str, remove_none=True))
        data_cls = dataclass(cls, init=False, **data_class_args)
        return data_cls

    if _cls is None:
        return wrap

    return wrap(_cls)
