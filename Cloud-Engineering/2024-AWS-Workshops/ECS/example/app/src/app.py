import os
from pathlib import Path

import joblib
import numpy as np
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import aws_utils as aws

# Load the Iris dataset and trained classifier
BUCKET_NAME = os.getenv("BUCKET_NAME", "smf2659-iris")
ARTIFACTS_PREFIX = Path(os.getenv("ARTIFACTS_PREFIX", "artifacts/"))
MODEL_VERSION = os.getenv("MODEL_VERSION", "default")

# Create artifacts directory to keep model files
artifacts = Path() / "artifacts"
artifacts.mkdir(exist_ok=True)
print("Loading artifacts from: ", artifacts.absolute())

# Set locations for each artifact file
iris_file = artifacts / "iris.joblib"
iris_model_file = artifacts / "iris_classifier.joblib"

# Configure S3 location for each artifact
iris_s3_key = str(ARTIFACTS_PREFIX / MODEL_VERSION / iris_file.name)
iris_model_s3_key = str(ARTIFACTS_PREFIX / MODEL_VERSION / iris_model_file.name)

# Download files from S3
aws.download_s3(BUCKET_NAME, iris_s3_key, iris_file)
aws.download_s3(BUCKET_NAME, iris_model_s3_key, iris_model_file)

# Load files into memory
iris = joblib.load(iris_file)
clf = joblib.load(iris_model_file)


# Define the input data schema
class InputData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Create the FastAPI app
app = FastAPI()


@app.get("/")
def root():
    return {
        "app": "iris-inference",
        "version": MODEL_VERSION,
        "model": f"s3://{BUCKET_NAME}/{iris_model_s3_key}",
        "data": f"s3://{BUCKET_NAME}/{iris_s3_key}",
    }

@app.get("/health")
def health():
    return {
        "health": "Application is healthy",
    }


@app.get("/classes")
def classes():
    return {"class_labels": list(iris.target_names)}


# Define the inference route
@app.post("/predict")
def predict(data: InputData):
    # Convert the input data to a NumPy array
    input_data = np.array(
        [data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]
    ).reshape(1, -1)

    # Make a prediction with the trained classifier
    prediction = clf.predict(input_data)[0]

    # Get the predicted class label and name
    class_label = int(prediction)
    class_name = str(iris.target_names[class_label])

    # Return the prediction as a JSON response
    return {"class_label": class_label, "class_name": class_name}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
