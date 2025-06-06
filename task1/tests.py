import pytest
from solution import strict


@strict
def add(a: int, b: int) -> int:
    return a + b


@strict
def hello(name: str):
    return f"Hello, {name}!"


def test_correct_types():
    assert add(1, 2) == 3
    assert hello("Ben") == "Hello, Ben!"


def test_incorrect_type_first_arg():
    with pytest.raises(TypeError):
        add("1", 2)


def test_incorrect_type_second_arg():
    with pytest.raises(TypeError):
        add(1, "2")


def test_incorrect_type_greet():
    with pytest.raises(TypeError):
        hello(123)
