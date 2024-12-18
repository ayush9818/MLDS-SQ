import testing_lab.example as base
import pandas as pd
import pytest


def test_capital_case_lower():
    assert base.capital_case("hello world") == "Hello world"


def test_capital_case_upper():
    assert base.capital_case(...)  # TODO: Finish this test


# TODO: Create one more test case
def test_capital_case_number():
    with pytest.raises(...):  # TODO: Test for proper exception
        base.capital_case(123)


def test_select_dataframe_column_single():
    df = pd.DataFrame(
        {
            "A": ["John", "Boby", "Mina"],
            "B": ["Masters", "Graduate", "Graduate"],
            "C": [27, 23, 21],
        }
    )
    result = base.select_dataframe_column(...)
    expected = ...
    assert result.equals(...)  # TODO: Finish test


# TODO: Create one more test case
