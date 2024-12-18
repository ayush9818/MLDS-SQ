import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st


app_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app/")
sys.path.insert(0, app_dir)
from app import get_user_inputs, display_prediction, main

# Mock Constants
MODEL_NAME = "v1"
AVAILABLE_MODELS = {
    "v1": "s3://your-bucket-path/model_v1.pkl",
    "v2": "s3://your-bucket-path/model_v2.pkl",
}


@pytest.fixture
def mock_streamlit(monkeypatch):
    """Fixture to mock Streamlit functions."""
    st_mock = MagicMock()
    monkeypatch.setattr(st, "sidebar", st_mock.sidebar)
    monkeypatch.setattr(st, "title", st_mock.title)
    monkeypatch.setattr(st, "selectbox", st_mock.selectbox)
    monkeypatch.setattr(st, "slider", st_mock.slider)
    monkeypatch.setattr(st, "button", st_mock.button)
    monkeypatch.setattr(st, "success", st_mock.success)
    monkeypatch.setattr(st, "metric", st_mock.metric)
    monkeypatch.setattr(st, "balloons", st_mock.balloons)
    monkeypatch.setattr(st, "error", st_mock.error)
    return st_mock


def test_get_user_inputs(mock_streamlit):
    """Test user inputs are correctly fetched from the sidebar."""
    mock_streamlit.sidebar.selectbox.return_value = MODEL_NAME
    mock_streamlit.sidebar.slider.side_effect = [5, 3, 7]

    model_name, log_entropy, IR_norm_range, entropy_x_contrast = get_user_inputs()

    mock_streamlit.sidebar.selectbox.assert_called_once_with(
        "Select Model", list(AVAILABLE_MODELS.keys())
    )
    assert mock_streamlit.sidebar.slider.call_count == 3
    assert model_name == MODEL_NAME
    assert log_entropy == 5
    assert IR_norm_range == 3
    assert entropy_x_contrast == 7


def test_display_prediction(mock_streamlit):
    """Test that the prediction is displayed correctly."""
    display_prediction("class_1")

    mock_streamlit.success.assert_called_once_with("Prediction Successful!")
    mock_streamlit.metric.assert_called_once_with(
        label="Model Prediction", value="class_1"
    )
    mock_streamlit.balloons.assert_called_once()


def test_get_model_error_handling(mock_streamlit):
    """Test error handling during model loading."""
    mock_streamlit.sidebar.selectbox.return_value = MODEL_NAME
    mock_streamlit.sidebar.slider.side_effect = [5, 3, 7]
    mock_streamlit.button.return_value = True

    # Mock the get_model function to raise an exception
    with patch(
        "app.get_model", side_effect=Exception("Model load failed")
    ) as mock_get_model:
        with pytest.raises(Exception, match="Model load failed"):
            main()
            mock_streamlit.error.assert_called_once_with(
                "Error during prediction: Model load failed"
            )
