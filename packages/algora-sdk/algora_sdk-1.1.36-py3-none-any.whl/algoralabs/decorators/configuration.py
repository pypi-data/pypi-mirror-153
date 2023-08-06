import dataclasses
from dataclasses import dataclass
from functools import partial, partialmethod
from typing import Optional

import pydash
import yaml
import os

from algoralabs.decorators.__util import __dataclass_to_json_str, __get_input, __initialize_data_class
from algoralabs.common.errors import InvalidConfig


def __load_yaml(file: Optional[str] = None) -> dict:
    """
    This function loads in a yaml file and returns the yaml represented as a dict

    Parameters:
        file: The yaml file location

    Returns:
         The dict representation of the yaml file
    """
    if file is None or not os.path.isfile(file):
        return {}

    with open(file, "r") as fp:
        yaml_object = yaml.safe_load(fp)
    return yaml_object


def __initializer(data_cls: dataclasses.dataclass, yaml_file: str, prefix: str, *args, **kwargs) -> None:
    """
    This is the __init__ function loaded in for object decorated as configurations

    Parameters:
         data_cls: Dataclass being initialized
         yaml_file: file location of the yaml used to populate the configuration class
         prefix: the prefix used to get the base data from the configuration file
         *args: The arg tuple passed to the method
         **kwargs: The keyword dictionary passed to the method
    """
    yaml_input = __get_input(partial(__load_yaml, file=yaml_file), **kwargs)
    inp: dict = (pydash.get(yaml_input, prefix) or yaml_input)
    __initialize_data_class(data_cls, inp, InvalidConfig)


def configuration(
        _cls: object = None,
        *,
        yaml_file: Optional[str] = None,
        prefix: Optional[str] = None,
        **data_class_args
) -> dataclasses.dataclass:
    """
    A decorator used to turn classes (modeled like dataclasses) to configurations objects

    Parameters:
        _cls: The class being decorated
        yaml_file: The yaml file use to populate the _cls (dataclass)
        prefix: The prefix in the yaml file used to get the lower level input in the file
        **data_class_args: keyword args passed to the dataclass constructor

    Returns:
        The updated class with the configuration methods
    """
    def wrap(cls):
        setattr(cls, "__init__", partialmethod(__initializer, yaml_file=yaml_file, prefix=prefix))
        setattr(cls, "__str__", partialmethod(__dataclass_to_json_str, remove_none=True))
        data_cls = dataclass(cls, init=False, **data_class_args)
        return data_cls

    if _cls is None:
        return wrap

    return wrap(_cls)

