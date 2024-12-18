import pytest

from example import inc


def test_inc():
    assert inc(3) == 4


def test_inc_nonnumeric():
    with pytest.raises(TypeError):
        inc("I am not a number")
