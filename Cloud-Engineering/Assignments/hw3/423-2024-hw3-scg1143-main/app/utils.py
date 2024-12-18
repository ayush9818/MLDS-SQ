import warnings

warnings.filterwarnings("ignore")

import pickle
import boto3
import os
import yaml
import logging

logger = logging.getLogger("app." + __name__)


def load_available_models():
    avail_models = yaml.full_load(open(os.getenv("AVAIL_MODELS", "config/models.yaml")))
    return avail_models["available_models"]


def download_model_from_s3(s3_path, local_path):
    """Download a model file from S3 to a local path."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("REGION_NAME"),
    )
    bucket_name, key = s3_path.replace("s3://", "").split("/", 1)
    s3.download_file(bucket_name, key, local_path)
    logger.info(f"File downloaded from {s3_path} to {local_path}")


def load_model(model_name, s3_path):
    """Load a model from S3 if not already loaded."""
    logger.info(f"Loading {model_name} model from {s3_path}")
    MODEL_STORE = os.getenv("MODEL_STORE", "models/")
    if not os.path.exists(MODEL_STORE):
        logger.info("Creating Model Store", MODEL_STORE)
        os.makedirs(MODEL_STORE)

    local_model_path = os.path.join(MODEL_STORE, f"{model_name}.pkl")

    if not os.path.exists(local_model_path):
        logger.info("Model does not exists. Downloading from s3")
        download_model_from_s3(s3_path, local_model_path)

    with open(local_model_path, "rb") as model_file:
        model = pickle.load(model_file)
        return model


def predict(model, input_data):
    """Generate a prediction from the model."""
    return model.predict([input_data])[0]
