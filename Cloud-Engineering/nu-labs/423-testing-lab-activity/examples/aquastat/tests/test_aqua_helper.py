import numpy as np
import pandas as pd
import pytest

import src.aqua_helper as aq

# Define expected input dataframe
df_in_values = [
    [
        "Indonesia",
        "World | Asia",
        "total_pop",
        "Total population (1000 inhab)",
        "1958-1962",
        1962.0,
        92558.0,
    ],
    [
        "Indonesia",
        "World | Asia",
        "total_pop",
        "Total population (1000 inhab)",
        "1963-1967",
        1967.0,
        105907.0,
    ],
    [
        "Indonesia",
        "World | Asia",
        "rural_pop",
        "Rural population (1000 inhab)",
        "1958-1962",
        1962.0,
        78538.0,
    ],
    [
        "Indonesia",
        "World | Asia",
        "rural_pop",
        "Rural population (1000 inhab)",
        "1963-1967",
        1967.0,
        88701.0,
    ],
    [
        "Indonesia",
        "World | Asia",
        "urban_pop",
        "Urban population (1000 inhab)",
        "1958-1962",
        1962.0,
        14020.0,
    ],
    [
        "Indonesia",
        "World | Asia",
        "urban_pop",
        "Urban population (1000 inhab)",
        "1963-1967",
        1967.0,
        17206.0,
    ],
    [
        "Indonesia",
        "World | Asia",
        "gdp",
        "Gross Domestic Product (GDP) (current US$)",
        "1958-1962",
        np.nan,
        np.nan,
    ],
    [
        "Indonesia",
        "World | Asia",
        "gdp",
        "Gross Domestic Product (GDP) (current US$)",
        "1963-1967",
        1967.0,
        5980840376.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "total_pop",
        "Total population (1000 inhab)",
        "1958-1962",
        1962.0,
        53147.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "total_pop",
        "Total population (1000 inhab)",
        "1963-1967",
        1967.0,
        54905.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "rural_pop",
        "Rural population (1000 inhab)",
        "1958-1962",
        1962.0,
        11474.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "rural_pop",
        "Rural population (1000 inhab)",
        "1963-1967",
        1967.0,
        12293.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "urban_pop",
        "Urban population (1000 inhab)",
        "1958-1962",
        1962.0,
        41673.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "urban_pop",
        "Urban population (1000 inhab)",
        "1963-1967",
        1967.0,
        42612.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "gdp",
        "Gross Domestic Product (GDP) (current US$)",
        "1958-1962",
        1962.0,
        80601939635.0,
    ],
    [
        "United Kingdom",
        "World | Europe",
        "gdp",
        "Gross Domestic Product (GDP) (current US$)",
        "1963-1967",
        1967.0,
        111000000000.0,
    ],
]

df_in_index = [
    3024,
    3025,
    3600,
    3601,
    4176,
    4177,
    4752,
    4753,
    102900,
    102901,
    103644,
    103645,
    104388,
    104389,
    105132,
    105133,
]

df_in_columns = [
    "country",
    "region",
    "variable",
    "variable_full",
    "time_period",
    "year_measured",
    "value",
]

df_in = pd.DataFrame(df_in_values, index=df_in_index, columns=df_in_columns)


def test_slice_by_time():
    # Define expected output, df_true
    df_true = pd.DataFrame(
        [[5980840376.0, 88701.0, 105907.0, 17206.0], [111000000000.0, 12293.0, 54905.0, 42612.0]],
        index=["Indonesia", "United Kingdom"],
        columns=["gdp", "rural_pop", "total_pop", "urban_pop"],
    )

    df_true.index.name = "country"
    df_true.columns.name = "1963-1967"

    # Compute test output

    df_test = aq.slice_by_time(df_in, "1963-1967")

    # Test that the true and test are the same
    pd.testing.assert_frame_equal(df_true, df_test)


def test_slice_by_time_empty():
    # What happens if no data given for provided time_period? e.g. '2013-2017'
    # Define expected output, df_true
    df_true = pd.DataFrame([], index=[], columns=[])

    df_true.columns.name = "2013-2017"
    df_true.index.name = "country"

    # Compute test output

    df_test = aq.slice_by_time(df_in, "2013-2017")

    # Test that the true and test are the same
    assert df_test.equals(df_true)


def test_slice_by_time_non_df():
    non_df_in = "I am not a dataframe"

    with pytest.raises(TypeError):
        aq.slice_by_time(non_df_in, "2013-2017")
