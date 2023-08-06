"""
lock-defaults - for python 3.10 + with paramspec for static typing

This file depends only on the standard library and can be copied
directly into a project.

Source: https://github.com/ajparsons/lock-defaults

Licence: MIT

"""
from collections.abc import MutableMapping, MutableSequence, MutableSet
from copy import deepcopy
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

WrappedReturnType = TypeVar("WrappedReturnType")
WrappedParameters = ParamSpec("WrappedParameters")


def lockmutabledefaults(
    func: Callable[WrappedParameters, WrappedReturnType]
) -> Callable[WrappedParameters, WrappedReturnType]:
    """
    Reset mutable defaults each time the function is called
    """
    # stash the original defaults
    # kwdefaults is for keyword *only* arguments
    original_defaults = func.__defaults__
    original_kwargs = func.__kwdefaults__

    # isinstance further down requires these not be typing Generics, so
    # so can't give new TypeVars to resolve the error here
    mutable_types: tuple[type, type, type]
    mutable_types = (MutableSequence, MutableSet, MutableMapping)  # type: ignore

    @wraps(func)  # preserve signature of new function
    def _inner(
        *args: WrappedParameters.args, **kwargs: WrappedParameters.kwargs
    ) -> WrappedReturnType:
        # redefine the defaults of the function
        # deepcopy any mutable objects from the original default
        if original_defaults:
            func.__defaults__ = tuple(
                [
                    deepcopy(x) if isinstance(x, mutable_types) else x
                    for x in original_defaults
                ]
            )
        if original_kwargs:
            func.__kwdefaults__ = {
                x: deepcopy(y) if isinstance(y, mutable_types) else y
                for x, y in original_kwargs.items()
            }
        # run the function
        result = func(*args, **kwargs)
        # the function may have modified the values currently in defaults
        # reset them or the signature is wrong if examined after use
        func.__defaults__ = original_defaults
        func.__kwdefaults__ = original_kwargs
        # return result of the function
        return result

    return _inner
