
import pytest

# Function to be tested
def add(a, b):
    return a + b

# Unit tests
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 5) == 4
    assert add(0, 0) == 0

# Fixture
@pytest.fixture
def setup_numbers():
    num1 = 10
    num2 = 5
    return num1, num2

# Parameterized test using fixture
@pytest.mark.parametrize("num1, num2, expected_result", [
    (1, 1, 2),
    (-1, 1, 0),
    (10, -5, 5)
])
def test_add_with_fixture(setup_numbers, num1, num2, expected_result):
    assert add(num1, num2) == expected_result

# Another parameterized test without using fixture
@pytest.mark.parametrize("num1, num2, expected_result", [
    (3, 2, 5),
    (5, 5, 10),
    (0, 0, 0)
])
def test_add_without_fixture(num1, num2, expected_result):
    assert add(num1, num2) == expected_result
