import warnings

warnings.filterwarnings("ignore")

import streamlit as st
from utils import load_model, predict, load_available_models
import json
import logging
import logging.config

logging.config.fileConfig("config/logging/local.ini", disable_existing_loggers=False)
logger = logging.getLogger("app." + __name__)

AVAILABLE_MODELS = load_available_models()


@st.cache_resource
def get_model(model_name, model_path):
    """Load and cache the model from S3."""
    return load_model(model_name, model_path)


def get_user_inputs():
    """Get user inputs from the sidebar."""
    st.sidebar.header("Model Selection and Parameters")
    model_name = st.sidebar.selectbox("Select Model", list(AVAILABLE_MODELS.keys()))
    log_entropy = st.sidebar.slider("log_entropy", -20.0, 0.0, 0.1)
    IR_norm_range = st.sidebar.slider("IR_norm_range", -200.0, 200.0, 0.1)
    entropy_x_contrast = st.sidebar.slider("entropy_x_contrast", 0.0, 400.0, 0.1)
    return model_name, log_entropy, IR_norm_range, entropy_x_contrast


def display_prediction(prediction):
    """Display the prediction result."""
    st.success("Prediction Successful!")
    st.metric(label="Model Prediction", value=f"{prediction}")
    st.balloons()


def main():
    st.title("ML Model Prediction App")

    # Get user inputs
    model_name, log_entropy, IR_norm_range, entropy_x_contrast = get_user_inputs()

    # Load and cache the selected model
    model = get_model(model_name, AVAILABLE_MODELS[model_name])

    # Prepare input data
    input_data = [log_entropy, IR_norm_range, entropy_x_contrast]

    # Predict button in main area
    if st.button("Predict"):
        try:
            logger.info(
                f"log_entropy : {log_entropy} -- IR_norm_range : {IR_norm_range} -- entropy_x_contrast : {entropy_x_contrast}"
            )
            prediction = predict(model, input_data)
            logger.info(f"Predicted Class : {prediction}")

            st.write(f"Selected Model: {model_name}")
            # Display prediction in a fancy way
            display_prediction(prediction)

        except Exception as e:
            logger.error("Prediction Failed", e)
            st.error(f"Error during prediction: {e}")


if __name__ == "__main__":
    main()
