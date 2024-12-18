import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.utils import to_categorical
from sklearn.datasets import load_iris
import pytest


# Fixture to load the Iris dataset
@pytest.fixture(scope="module")
def iris_data():
    # Load the Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target
    yield X, y

# Fixture to split the Iris dataset into training and testing sets
@pytest.fixture(scope="module")
def split_data(iris_data):
    X, y = iris_data
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    yield X_train, X_test, y_train, y_test

# Fixture to create a neural network model
@pytest.fixture(scope="module")
def model():
    # Create a neural network model
    model = Sequential()
    model.add(Dense(20, input_shape=(4,)))
    model.add(Activation('sigmoid'))
    model.add(Dense(3))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy', metrics=["accuracy"])
    yield model

# Test case to check the shape of the loaded Iris data
def test_data_shape(iris_data):
    X, y = iris_data
    # Check that the feature matrix has 4 columns and the target vector has 3 unique values
    assert X.shape[1] == 4
    assert len(np.unique(y)) == 3

# Test case to check the accuracy of the trained model
def test_model_accuracy(model, split_data):
    X_train, X_test, y_train, y_test = split_data
    y_train_ohe = to_categorical(y_train)
    model.fit(X_train, y_train_ohe, epochs=20, batch_size=5, verbose=0)
    loss, accuracy = model.evaluate(X_test, to_categorical(y_test), verbose=0)
    # Check that the accuracy is greater than 0.8
    assert accuracy > 0.4

# Test case to check the shape of the model predictions
def test_model_predictions(model, split_data):
    X_train, X_test, y_train, y_test = split_data
    y_train_ohe = to_categorical(y_train)
    model.fit(X_train, y_train_ohe, epochs=10, batch_size=5, verbose=0)
    predictions = model.predict(X_test)
    # Check that the predictions have the correct shape
    assert predictions.shape[0] == X_test.shape[0]
    assert predictions.shape[1] == 3