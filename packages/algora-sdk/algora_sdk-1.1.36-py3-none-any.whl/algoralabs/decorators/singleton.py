import functools
from functools import partial
from typing import Callable, Optional, Dict, Any, NewType

Constructor = NewType('Constructor', Callable[[Any], object])


def singleton(cls: Optional[Constructor] = None) -> Constructor:
    """
    A decorator used to make classes singleton (i.e. all instances refer to the same instance)

    Args:
        cls: The class that is supposed to be a singleton

    Returns:
        A constructor that creates the first object instance or returns the already created object
    """
    instances: Dict[Constructor, object] = {}

    @functools.wraps(cls)
    def wrap(_cls: Constructor, *args, **kwargs) -> object:
        """
        Wrapper that checks to see if the object exists and if it doesnt it creates it one

        Args:
            _cls: The singleton class
            *args: Args for the class constructor
            **kwargs: The keyword arguments for the class constructor

        Returns:
            The new class instance or the already existing class instance
        """
        if _cls not in instances:
            instances[_cls] = _cls(*args, **kwargs)
        return instances[_cls]

    if cls is None:
        return wrap

    return partial(wrap, cls)
