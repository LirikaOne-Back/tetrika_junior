import pytest
from solution import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def greet(name: str, excited: bool) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"


def test_sum_two_ok():
    assert sum_two(1, 2) == 3


def test_sum_two_type_error():
    with pytest.raises(TypeError) as e:
        sum_two(1, 2.0)
    assert "Argument 'b' must be of type int" in str(e.value)


def test_greet_ok():
    assert greet("Alice", False) == "Hello, Alice."


def test_greet_bool_strict():
    with pytest.raises(TypeError):
        greet(123, True)


def test_keyword_args():
    assert sum_two(a=5, b=7) == 12
    with pytest.raises(TypeError):
        sum_two(a=5, b="7")
