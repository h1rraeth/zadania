import pytest
from utils import add, subtract, multiply, divide

def test_add():
    assert add(5, 3) == 8
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(10, 4) == 6

def test_multiply():
    assert multiply(3, 7) == 21

def test_divide():
    assert divide(12, 3) == 4.0
    with pytest.raises(ValueError):
        divide(10, 0)