#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import logging
import time
from config_reader import ConfigReader

logging.basicConfig(level=logging.INFO)

class ModelConfig:
    def __init__(self, config):
        self.epochs = int(config['epochs'])

def measure_time(func):
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info("Function %s executed in %.4f seconds", func.__name__, execution_time)
        return result
    return wrapper

@measure_time
def load_data():
    """Load the Iris dataset and extract features and target."""
    try:
        iris = datasets.load_iris()
        X = iris.data[:, :2]  # We only take the first two features
        y = iris.target
        logging.info("Data loaded successfully")
        return X, y
    except Exception as e:
        logging.error("Error loading data: %s", str(e))
        return None, None

@measure_time
def preprocess_data(X, y):
    """Preprocess data by splitting into train and test sets, and one-hot encoding target."""
    try:
        encoder = OneHotEncoder()
        y_ohe = encoder.fit_transform(y.reshape(-1, 1)).toarray()
        X_train, X_test, y_train, y_test = train_test_split(X, y_ohe, test_size=0.3, random_state=0)
        logging.info("Data preprocessed successfully")
        return X_train, X_test, y_train, y_test
    except Exception as e:
        logging.error("Error preprocessing data: %s", str(e))
        return None, None, None, None

@measure_time
def build_model():
    """Build and compile the neural network model."""
    try:
        model = Sequential([
            Dense(16, input_shape=(2,), activation='sigmoid'),
            Dense(3, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=["accuracy"])
        logging.info("Model built successfully")
        return model
    except Exception as e:
        logging.error("Error building model: %s", str(e))
        return None

@measure_time
def train_model(model, X_train, y_train, config):
    """Train the neural network model."""
    try:
        model.fit(X_train, y_train, epochs=config.epochs, batch_size=5, verbose=1)
        logging.info("Model trained successfully")
        return model
    except Exception as e:
        logging.error("Error training model: %s", str(e))
        return None

@measure_time
def evaluate_model(model, X_test, y_test):
    """Evaluate the trained model on the test data."""
    try:
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        logging.info("Model evaluated successfully")
        return loss, accuracy
    except Exception as e:
        logging.error("Error evaluating model: %s", str(e))
        return None, None

@measure_time
def predict(model, X_test):
    """Make predictions using the trained model."""
    try:
        predictions = model.predict(X_test)
        predicted_classes = np.argmax(predictions, axis=-1)
        logging.info("Predictions made successfully")
        return predicted_classes
    except Exception as e:
        logging.error("Error making predictions: %s", str(e))
        return None

def main(environment):
    """Main function to execute the workflow."""
    try:
        # Load configuration
        config_reader = ConfigReader()
        config_dict = config_reader.load_config(environment)
        if config_dict is None:
            raise ValueError(f"Failed to load configuration for environment '{environment}'")

        config = ModelConfig(config_dict)

        # Load data
        X, y = load_data()
        if X is None or y is None:
            raise ValueError("Failed to load data")

        # Preprocess data
        X_train, X_test, y_train, y_test = preprocess_data(X, y)
        if X_train is None or X_test is None or y_train is None or y_test is None:
            raise ValueError("Failed to preprocess data")

        # Build model
        model = build_model()
        if model is None:
            raise ValueError("Failed to build model")

        # Train model
        model = train_model(model, X_train, y_train, config)
        if model is None:
            raise ValueError("Failed to train model")

        # Evaluate model
        loss, accuracy = evaluate_model(model, X_test, y_test)
        if loss is None or accuracy is None:
            raise ValueError("Failed to evaluate model")

        # Make predictions
        predicted_classes = predict(model, X_test)
        if predicted_classes is None:
            raise ValueError("Failed to make predictions")

        # Print confusion matrix
        confusion_matrix = pd.crosstab(index=y_test.argmax(axis=1), columns=predicted_classes, rownames=['Expected'], colnames=['Predicted'])
        print("Confusion Matrix:\n", confusion_matrix)
        logging.info("Workflow completed successfully")
    except Exception as e:
        logging.error("Error in main workflow: %s", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <environment>")
        sys.exit(1)

    environment = sys.argv[1]  # Get the environment argument from command line
    main(environment)
