import pytest
import requests_mock
from src.data_fetcher import (
    get_data,
    acquire_data,
)


# Tests for get_data
def test_get_data_success():
    """Test that get_data correctly fetches data when the request succeeds."""
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("http://example.com", text="data", status_code=200)
        assert (
            get_data("http://example.com") == b"data"
        ), "get_data should return the response content."


def test_get_data_retry_fail():
    """Test that get_data raises a RuntimeError after all retries fail."""
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("http://example.com", status_code=500)
        with pytest.raises(RuntimeError) as exc_info:
            get_data("http://example.com", attempts=2)
        assert "Failed to fetch data after 2 attempts." in str(
            exc_info.value
        ), "get_data should raise RuntimeError when all retries fail."


# Tests for acquire_data
def test_acquire_data_success(tmp_path):
    """Test that acquire_data saves the data to the specified file path."""
    test_content = b"example data"
    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("http://example.com", content=test_content, status_code=200)
        test_file = tmp_path / "testfile"
        acquire_data("http://example.com", test_file)
        assert (
            test_file.read_bytes() == test_content
        ), "acquire_data should write the content correctly to the file."


def test_acquire_data_file_not_found(tmp_path):
    """Test that acquire_data raises FileNotFoundError if the path is invalid."""
    with requests_mock.Mocker() as mock_requests:
        # Mocking the URL even though we expect the test to fail on writing to an invalid path
        mock_requests.get("http://example.com", text="data", status_code=200)

        test_file = tmp_path / "nonexistent_directory" / "testfile"
        with pytest.raises(FileNotFoundError) as exc_info:
            acquire_data("http://example.com", test_file)
        assert "Invalid file location provided." in str(
            exc_info.value
        ), "acquire_data should raise FileNotFoundError when the save path is invalid."
