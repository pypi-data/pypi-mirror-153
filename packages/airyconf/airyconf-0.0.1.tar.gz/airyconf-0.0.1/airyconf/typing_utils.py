import typing
from typing import Any
from dataclasses import is_dataclass
import builtins

from airyconf.typing_compat import get_origin, get_args

_BUILTIN_TYPES = tuple(getattr(builtins, t) for t in dir(builtins) if isinstance(getattr(builtins, t), type))


def is_builtin_type(tp: type) -> bool:
    """
    Checks if tp is a builtin type.

    >>> is_builtin_type(int)
    True
    >>> is_builtin_type(list)
    True
    >>> is_builtin_type(typing.Tuple[int])
    False
    """
    return tp in _BUILTIN_TYPES


def is_generic(cls) -> bool:
    """
    Detects any kind of generic, for example `List` or `List[int]`. This includes "special" types like
    Union and Tuple - anything that's subscriptable.

    >>> is_generic(typing.List[int])
    True
    >>> is_generic(typing.Tuple)
    True
    >>> is_generic(int)
    False
    >>> is_generic(list)
    False
    """
    return get_origin(cls) is not None


def is_base_generic(cls) -> bool:
    """
    Detects generic base classes, for example `List` (but not `List[int]`)

    >>> is_base_generic(typing.List)
    True
    >>> is_base_generic(typing.List[int])
    False
    >>> is_base_generic(int)
    False
    """
    return (get_origin(cls) is not None) and not get_args(cls)


def is_qualified_generic(cls) -> bool:
    """
    Detects generics with arguments, for example `List[int]` (but not `List`)

    >>> is_qualified_generic(typing.List)
    False
    >>> is_qualified_generic(typing.List[int])
    True
    >>> is_qualified_generic(int)
    False
    """
    return is_generic(cls) and not is_base_generic(cls)


def get_generic_arg(cls):
    """
    Return a **single** generic argument for parsing. For Dict only return the second argument; ignores Ellipsis.
    Therefore, does **not** support multiple arguments (e.g., Union[int, str, float]). Subject to changes.

    >>> get_generic_arg(typing.List[int])
    <class 'int'>
    >>> get_generic_arg(typing.Tuple[str, ...])
    <class 'str'>
    >>> get_generic_arg(typing.Dict[str, float])
    <class 'float'>
    >>> get_generic_arg(typing.Union[str, float])
    <class 'float'>
    >>> get_generic_arg(int)
    ()
    """

    args = get_args(cls)
    if not args:
        return args
    args = tuple(filter(lambda a: a != Ellipsis, args))
    args = args[-1]

    return args


def is_dataclass_type(cls: Any) -> bool:
    return is_dataclass(cls) and isinstance(cls, type)


def is_dataclass_instance(obj: Any) -> bool:
    return is_dataclass(obj) and not isinstance(obj, type)


def is_annotated_constructor(cls) -> bool:
    return hasattr(cls, '__init__') and hasattr(cls.__init__, '__annotations__')


if __name__ == '__main__':
    import doctest

    doctest.testmod()
