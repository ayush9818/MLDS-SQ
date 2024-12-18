import pytest
import pandas as pd
from src.create_dataset import (
    create_dataset,
    save_dataset,
)


def setup_raw_data(tmp_path):
    """
    Fixture to setup a temporary raw data file for testing.

    Args:
        tmp_path (LocalPath): A pytest fixture that provides a temporary directory unique to the test invocation.

    Returns:
        Path: The path to the temporary raw data file.
    """
    data_path = tmp_path / "data.txt"
    with open(data_path, "w") as f:
        f.write("1 2 3\n4 5 6\n7 8 9\n10 11 12\n")
    return data_path


def test_create_dataset_successful(tmp_path):
    """
    Test the happy path for create_dataset to ensure it processes data correctly.
    """
    config = {
        "columns": ["feature1", "feature2", "feature3"],
        "classes": [
            {"start": 0, "end": 2, "label": 0},
            {"start": 2, "end": 4, "label": 1},
        ],
    }
    result = create_dataset(str(setup_raw_data(tmp_path)), config)
    expected_data = {
        "feature1": [1.0, 4.0, 7.0, 10.0],
        "feature2": [2.0, 5.0, 8.0, 11.0],
        "feature3": [3.0, 6.0, 9.0, 12.0],
        "target": [0, 0, 1, 1],
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_create_dataset_missing_columns(tmp_path):
    """
    Test create_dataset for handling missing column configurations.
    """
    config = {"columns": [], "classes": [{"start": 0, "end": 2, "label": 0}]}
    with pytest.raises(ValueError) as exc_info:
        _ = create_dataset(str(setup_raw_data(tmp_path)), config)
    assert "Column names are missing in the configuration." in str(exc_info.value)


def test_create_dataset_file_not_found():
    """
    Test create_dataset for handling non-existent file path.
    """
    config = {
        "columns": ["feature1", "feature2", "feature3"],
        "classes": [{"start": 0, "end": 2, "label": 0}],
    }
    non_existent_path = "nonexistent_file.txt"
    with pytest.raises(FileNotFoundError):
        _ = create_dataset(non_existent_path, config)


def test_save_dataset_successful(tmp_path):
    """
    Test the happy path for save_dataset to ensure it saves data correctly.
    """
    df = pd.DataFrame({"feature1": [1, 2], "feature2": [3, 4]})
    data_path = tmp_path / "test_data.csv"
    save_dataset(df, data_path)
    saved_df = pd.read_csv(data_path)
    pd.testing.assert_frame_equal(df, saved_df)


def test_save_dataset_unsupported_format(tmp_path):
    """
    Test save_dataset for handling unsupported file formats.
    """
    df = pd.DataFrame({"feature1": [1, 2], "feature2": [3, 4]})
    data_path = tmp_path / "test_data.unsupported"
    with pytest.raises(ValueError) as exc_info:
        save_dataset(df, data_path)
    assert "Unsupported file format" in str(exc_info.value)
