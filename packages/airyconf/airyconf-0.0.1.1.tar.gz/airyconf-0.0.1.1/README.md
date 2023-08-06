# _airyconf_

## Lightweight configuration manager

Inspired by [zifeo/dataconf](https://github.com/zifeo/dataconf), 
implemented with no required dependencies for Python 3.6+ 
(except Python 3.6 requires dataclasses package to support the corresponding functionality). Supports typing, dataclasses and custom classes:


```python
from typing import List
from dataclasses import dataclass
from airyconf import parse


class CustomObject(object):
    def __init__(self, a: float):
        self.a = a
    
    def __eq__(self, other):
        return isinstance(other, CustomObject) and other.a == self.a

@dataclass
class SomeDataclass:
    b: str
    c: List[CustomObject]

json_config = '{"SomeDataclass": {"b": "str", "c": [{"a": 1.0}, {"a": 2.0}]}}'

expected = SomeDataclass('str', [CustomObject(1.), CustomObject(2.)])

assert parse(json_config, SomeDataclass) == expected

```

Optionally, supports yaml if installed:

```python
from airyconf import parse_config
parse_config('file/to/config.yaml', SomeDataclass)
```

Thanks to 
[rossmacarthur/typing-compat](https://github.com/rossmacarthur/typing-compat)
by Ross MacArthur, 
typing is supported for Python 3.6+ (the single-file package is copied to avoid dependencies).

### _Package is under development. TODO:_

- Add documentation
- Github actions: tests & coverage & package update
- Multiple typing arguments (```Tuple[int, CustomClass, str]```)
- Nested typing arguments (```List[Dict[str, List[int]]]```)
- Specify classes in config (```a: SomeCustomClass({param: 1})```)
