import pytest
import pandas as pd
import numpy as np
from src.generate_features import (
    FeatureGenerator,
)


def feature_generator():
    """Fixture to create a DataFrame and instantiate the FeatureGenerator for use in all tests."""
    data = pd.DataFrame({"A": [0, 1, 2, 3], "B": [4, 5, 6, 7], "C": [2, 3, 4, 5]})
    return FeatureGenerator(data)


def test_calculate_norm_range_happy():
    """
    Test calculate_norm_range with correct parameters to ensure it calculates normalized range as expected.
    """
    params = {"min_col": "A", "max_col": "B", "mean_col": "C"}
    fg = feature_generator()
    fg.calculate_norm_range("norm_range", params)
    expected_result = (fg.data["B"] - fg.data["A"]) / fg.data["C"]
    expected_result.name = "norm_range"
    pd.testing.assert_series_equal(fg.data["norm_range"], expected_result)


def test_calculate_norm_range_unhappy():
    """
    Test calculate_norm_range with a reference to a non-existent column to check for KeyError.
    """
    params = {"min_col": "A", "max_col": "Z", "mean_col": "C"}  # 'Z' does not exist
    fg = feature_generator()
    with pytest.raises(KeyError):
        fg.calculate_norm_range("norm_range", params)


def test_calculate_range_happy():
    """
    Test calculate_range with correct parameters to ensure it calculates the range correctly.
    """
    params = {"min_col": "A", "max_col": "B"}
    fg = feature_generator()
    fg.calculate_range("range", params)
    expected_result = fg.data["B"] - fg.data["A"]
    expected_result.name = "range"
    pd.testing.assert_series_equal(fg.data["range"], expected_result)


def test_calculate_range_unhappy():
    """
    Test calculate_range with a reference to a non-existent column to check for KeyError.
    """
    params = {"min_col": "X", "max_col": "B"}  # 'X' does not exist
    fg = feature_generator()
    with pytest.raises(KeyError):
        fg.calculate_range("range", params)


def test_log_transform_happy():
    """
    Test log_transform with correct column to ensure it applies the natural logarithm correctly.
    """
    fg = feature_generator()
    fg.log_transform("log_C", "C")
    expected_result = np.log(fg.data["C"])
    expected_result.name = "log_C"
    pd.testing.assert_series_equal(fg.data["log_C"], expected_result)


def test_log_transform_unhappy():
    """
    Test log_transform with a reference to a non-existent column to check for KeyError.
    """
    fg = feature_generator()
    with pytest.raises(KeyError):
        fg.log_transform("log_Z", "Z")  # 'Z' does not exist


def test_multiply_columns_happy():
    """
    Test multiply_columns with correct columns to ensure it multiplies columns correctly.
    """
    params = {"col_a": "A", "col_b": "B"}
    fg = feature_generator()
    fg.multiply_columns("product", params)
    expected_result = fg.data["A"] * fg.data["B"]
    expected_result.name = "product"
    pd.testing.assert_series_equal(fg.data["product"], expected_result)


def test_multiply_columns_unhappy():
    """
    Test multiply_columns with a reference to a non-existent column to check for KeyError.
    """
    params = {"col_a": "A", "col_b": "Z"}  # 'Z' does not exist
    fg = feature_generator()
    with pytest.raises(KeyError):
        fg.multiply_columns("product", params)
