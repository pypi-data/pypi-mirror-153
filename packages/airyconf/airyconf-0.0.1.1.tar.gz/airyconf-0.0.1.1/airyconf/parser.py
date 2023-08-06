from airyconf.loaders import get_loader, json_loader, LOADER_TYPE
from airyconf.typing_utils import (
    is_builtin_type,
    is_generic,
    get_generic_arg,
    is_dataclass_type,
    get_origin,
    is_annotated_constructor,
)

__all__ = [
    'parse',
    'parse_config',
]


def parse_config(
        path, config_cls: type, *, loader: LOADER_TYPE = None,
):
    with open(str(path), 'r') as f:
        conf_str = f.read()

    loader = loader or get_loader(path)

    return parse(conf_str, config_cls, loader=loader)


def parse(
        conf_string: str,
        config_cls: type, *,
        loader: LOADER_TYPE = json_loader,
):
    conf_dict = loader(conf_string)

    if hasattr(config_cls, '__name__'):
        try:
            conf_dict = conf_dict[config_cls.__name__]
        except KeyError:
            pass

    parsed_obj = _parse_annotated_constructor(conf_dict, config_cls)

    return parsed_obj


def _parse_annotated_constructor(conf_args: dict, cls):
    assert _is_supported_constructor(cls), f'Unsupported constructor {cls}'

    kwargs = {k: _parse_element(k, v, cls) for k, v in conf_args.items()}
    instance = cls(**kwargs)
    return instance


def _parse_element(key, value, datacls):
    annotation = _get_key_annotation(key, datacls)
    origin = get_origin(annotation)
    nested_cls = get_generic_arg(annotation)

    if is_builtin_type(annotation):
        return value

    elif is_builtin_type(nested_cls):
        return origin(value)

    elif origin in (list, tuple):
        return origin(_parse_annotated_constructor(v, nested_cls) for v in value)

    elif origin == dict:
        return {k: _parse_annotated_constructor(v, nested_cls) for k, v in value.items()}

    elif _is_supported_constructor(annotation):
        assert isinstance(value, dict), f'Wrong value: {value}'
        return _parse_annotated_constructor(value, annotation)

    raise ValueError(f'Unsupported annotation {annotation}')


def _get_key_annotation(key: str, cls):
    try:
        return _get_constructor_annotations(cls)[key]
    except KeyError:
        raise KeyError(f'Unexpected key {key}')


def _get_constructor_annotations(cls):
    if is_dataclass_type(cls):
        return cls.__annotations__
    elif is_annotated_constructor(cls):
        return cls.__init__.__annotations__
    else:
        raise ValueError(f'Unsupported constructor {cls}')


def _is_supported_constructor(cls):
    return (
            not (is_builtin_type(cls) or is_generic(cls))
            and (is_dataclass_type(cls) or is_annotated_constructor(cls))
    )
