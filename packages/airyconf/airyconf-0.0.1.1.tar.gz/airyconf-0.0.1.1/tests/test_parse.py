from typing import List, Tuple, Dict
import unittest

from dataclasses import dataclass

from airyconf import parse


class TestParser(unittest.TestCase):
    def test_flat_dataclass(self):
        @dataclass
        class A:
            a: float
            b: str

        config = '{"A": {"a": 1.0, "b": "string"}}'

        parsed = parse(config, A)
        expected = A(1, 'string')

        self.assertEqual(parsed, expected)

    def test_nested_dataclass(self):
        @dataclass
        class SecondLevel:
            c: float

        @dataclass
        class FirstLevel:
            b1: SecondLevel
            b2: SecondLevel
            b3: str

        @dataclass
        class A:
            a: FirstLevel

        config = '{"A": {"a": {"b1": {"c": 1.0}, "b2": {"c": 2.0}, "b3": "string"}}}'

        parsed = parse(config, A)
        expected = A(
            FirstLevel(
                SecondLevel(1.),
                SecondLevel(2.),
                "string",
            )
        )

        self.assertEqual(parsed, expected)

    def test_nested_typings(self):
        @dataclass
        class FirstLevel:
            d: float

        @dataclass
        class A:
            a: List[FirstLevel]
            b: List[int]
            c: Dict[str, FirstLevel]

        config = '{"A": {"a": [{"d": 1.0}, {"d": 2.0}], "b": [1, 2], "c": {"key": {"d": 3.0}}}}'

        parsed = parse(config, A)

        expected = A(
            a=[FirstLevel(1.), FirstLevel(2.)],
            b=[1, 2],
            c={'key': FirstLevel(3.)}
        )

        self.assertEqual(parsed, expected)

    def test_deep_nested_typings(self):
        @dataclass
        class SecondLevel:
            c: int

        @dataclass
        class FirstLevel:
            a: List[SecondLevel]
            b: List[int]
            c: str

        @dataclass
        class A:
            a: List[FirstLevel]
            b: Tuple[int, ...]
            c: Dict[str, FirstLevel]

        config = '''{"A": {"a": 
        [
            {"a": [{"c": 1}, {"c": 2}], "b": [1, 2, 3], "c": "string_1"},
            {"a": [{"c": 3}], "b": [1], "c": "string_2"}
        ],
        "b": [3, 4, 5],
        "c": {"key": {"a": [{"c": 1}, {"c": 2}], "b": [1, 2, 3], "c": "string_1"}}
        }}'''.replace('\n', '')

        first_level1 = FirstLevel(
            [
                SecondLevel(1),
                SecondLevel(2),
            ],
            b=[1, 2, 3],
            c='string_1'
        )

        first_level2 = FirstLevel(
            [
                SecondLevel(3),
            ],
            b=[1, ],
            c='string_2'
        )

        parsed = parse(config, A)

        expected = A(
            a=[first_level1, first_level2],
            b=(3, 4, 5),
            c={'key': first_level1}
        )

        self.assertEqual(parsed, expected)

    def test_custom_classes(self):
        class C(object):
            def __init__(self, e: float):
                self.e = e

            def __eq__(self, other):
                return isinstance(other, C) and other.e == self.e

        @dataclass
        class B:
            c: C
            d: int

        class A(object):
            def __init__(self, a: str, b: B):
                self.a = a
                self.b = b

            def __eq__(self, other):
                return isinstance(other, A) and other.a == self.a and other.b == self.b

            def __repr__(self):
                return f'A({self.a}, {self.b})'

        config = '{"A": {"a": "string", "b": {"c": {"e": 1.0}, "d": 2}}}'

        parsed = parse(config, A)

        expected = A(
            a='string',
            b=B(C(1.), 2),
        )

        self.assertEqual(parsed, expected)

    @unittest.skip("Does not support nested typing arguments yet!")
    def test_nested_typing_arguments(self):
        @dataclass
        class A:
            a: List[Dict[str, List[int]]]

        json_config = '{"A": {"a": [{"b": [1, 2, 3]}]}}'

        expected = A([{'b': [1, 2, 3]}])

        parsed = parse(json_config, A)

        self.assertEqual(parsed, expected)

    def test_readme_example(self):
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

        self.assertEqual(parse(json_config, SomeDataclass), expected)


if __name__ == '__main__':
    unittest.main()
