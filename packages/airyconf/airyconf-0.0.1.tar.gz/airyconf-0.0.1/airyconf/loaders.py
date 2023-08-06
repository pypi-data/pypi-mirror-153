import json
from typing import Union, Callable
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


LOADER_TYPE = Callable[[str, ], dict]


def json_loader(conf_str: str):
    return json.loads(conf_str)


def yaml_loader(conf_str: str):
    if not yaml:
        raise ImportError('PyYaml is not installed')
    return yaml.safe_load(conf_str)


def get_loader(file_path: Union[Path, str]):
    suffix = Path(file_path).suffix
    if suffix == '.json':
        return json_loader
    if suffix == 'yaml':
        return yaml_loader
