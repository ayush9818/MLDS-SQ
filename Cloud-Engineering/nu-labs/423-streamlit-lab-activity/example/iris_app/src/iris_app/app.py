import os
from pathlib import Path

import streamlit as st
import joblib
import numpy as np

# Load the Iris dataset and trained classifier
BUCKET_NAME = os.getenv("BUCKET_NAME", "smf2659-iris")
ARTIFACTS_PREFIX = Path(os.getenv("ARTIFACTS_PREFIX", "artifacts/"))

# Create artifacts directory to keep model files
artifacts = Path() / "artifacts"
artifacts.mkdir(exist_ok=True)


def load_data(data_file):
    print("Loading artifacts from: ", artifacts.absolute())

    # Load files into memory
    iris = joblib.load(data_file)
    X: np.ndarray = iris.data
    class_names = iris.target_names

    return class_names, X


def load_model(model_file):
    # Download files from S3
    clf = joblib.load(model_file)
    return clf


def slider_values(series) -> tuple[float, float, float]:
    return (
        float(series.min()),
        float(series.max()),
        float(series.mean()),
    )


# Create the application title and description
st.title("Iris Flower Species Prediction")
st.write("This app predicts the species of an iris flower based on its measurements.")

st.subheader("Model Selection")
model_version = os.getenv("DEFAULT_MODEL_VERSION", "default")
st.write(f"Selected model version: {model_version}")

# Establish the dataset and TMO locations based on selection
iris_file = artifacts / model_version / "iris.joblib"
iris_model_file = artifacts / model_version / "iris_classifier.joblib"

# Load the dataset and TMO into memory
class_names, X = load_data(iris_file)
clf = load_model(iris_model_file)

# Sidebar inputs for feature values
st.sidebar.header("Input Parameters")
sepal_length = st.sidebar.slider("Sepal length", *slider_values(X[:, 0]))
sepal_width = st.sidebar.slider("Sepal width", *slider_values(X[:, 1]))
petal_length = st.sidebar.slider("Petal length", *slider_values(X[:, 2]))
petal_width = st.sidebar.slider("Petal width", *slider_values(X[:, 3]))

# Make predictions on user inputs
input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
prediction = clf.predict(input_data)
predicted_class = class_names[prediction[0]]

# Display the predicted class and probability
st.subheader("Prediction")
st.write(f"Predicted Class: {predicted_class}")
st.write(f"Probability: {clf.predict_proba(input_data)[0][prediction[0]]:.2f}")
