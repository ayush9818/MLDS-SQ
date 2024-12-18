import pytest
import os
import sys
import pickle
import boto3
from unittest.mock import patch, MagicMock

app_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app/")
sys.path.insert(0, app_dir)


from utils import load_model, predict, load_available_models, download_model_from_s3

# Constants
MODEL_NAME = "model_v1"
S3_PATH = "s3://your-bucket-path/model_v1.pkl"
MODEL_DATA = [1, 2, 3]


class MockModel:
    """Mock model class for testing purposes."""

    def predict(self, input_data):
        """Mock predict method that sums the input data."""
        return [sum(input_data[0])]


@pytest.fixture
def mock_boto3_client(monkeypatch):
    """Fixture to mock the boto3 client for S3 interactions."""
    mock_client = MagicMock()
    mock_client.download_file = MagicMock()
    monkeypatch.setattr("boto3.client", lambda *args, **kwargs: mock_client)
    return mock_client


@pytest.fixture
def mock_model():
    """Fixture to provide a mock model instance."""
    return MockModel()


@pytest.fixture
def setup_model_store(tmpdir):
    """Fixture to set up a temporary model store directory."""
    model_store = tmpdir.mkdir("models")
    os.environ["MODEL_STORE"] = str(model_store)
    return model_store


def test_load_available_models(monkeypatch):
    """
    Test that the available models are loaded correctly from the YAML configuration.
    """
    yaml_content = """
    available_models:
      model_v1: "s3://your-bucket-path/model_v1.pkl"
      model_v2: "s3://your-bucket-path/model_v2.pkl"
    """
    monkeypatch.setattr("builtins.open", lambda f: yaml_content)
    models = load_available_models()
    assert models == {
        "model_v1": "s3://your-bucket-path/model_v1.pkl",
        "model_v2": "s3://your-bucket-path/model_v2.pkl",
    }


def test_download_model_from_s3(mock_boto3_client, setup_model_store):
    """
    Test that the model file is downloaded from S3 to the specified local path.
    """
    local_model_path = os.path.join(setup_model_store, f"{MODEL_NAME}.pkl")

    # Mock the behavior of download_model_from_s3 to simulate file download
    with patch(
        "utils.download_model_from_s3", wraps=download_model_from_s3
    ) as mock_download:
        # Call the actual function which will now use the mock client
        download_model_from_s3(S3_PATH, local_model_path)

        # Simulate file creation to represent a successful download
        with open(local_model_path, "w") as f:
            f.write("dummy content")

        # Assert that the S3 download method was called with the correct parameters
        mock_boto3_client.download_file.assert_called_once_with(
            "your-bucket-path", "model_v1.pkl", local_model_path
        )
        # Assert that the file now exists at the local path
        assert os.path.exists(local_model_path)


def test_load_model(mock_boto3_client, setup_model_store, mock_model):
    """
    Test that the model is loaded correctly from the local file system and can make predictions.
    """
    local_model_path = os.path.join(setup_model_store, f"{MODEL_NAME}.pkl")
    with open(local_model_path, "wb") as f:
        pickle.dump(mock_model, f)

    model = load_model(MODEL_NAME, S3_PATH)
    assert model.predict([MODEL_DATA]) == [sum(MODEL_DATA)]


def test_predict_with_invalid_input(mock_model):
    """
    Test that the predict function raises an exception when given invalid input data.
    """
    input_data = ["invalid", "input", "data"]
    with pytest.raises(Exception):
        predict(mock_model, [input_data])


def test_load_model_raises_exception_on_failure(mock_boto3_client, setup_model_store):
    """
    Test that an exception is raised when the model download from S3 fails.
    """
    local_model_path = os.path.join(setup_model_store, f"{MODEL_NAME}.pkl")
    mock_boto3_client.download_file.side_effect = Exception("Download failed")
    with pytest.raises(Exception, match="Download failed"):
        load_model(MODEL_NAME, S3_PATH)
