import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.utils import to_categorical
from sklearn.datasets import load_iris

class IrisClassifier:
    def __init__(self):
        self.model = None

    def load_data(self):
        # Load the Iris dataset
        iris = load_iris()
        X = iris.data
        y = iris.target
        return X, y

    def split_data(self, X, y, test_size=0.3, random_state=42):
        # Split the dataset into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def create_model(self, input_shape, num_classes):
        # Create a neural network model
        model = Sequential()
        model.add(Dense(16, input_shape=input_shape))
        model.add(Activation('sigmoid'))
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))
        return model

    def train_model(self, X_train, y_train, epochs=10, batch_size=5):
        # Categorical data must be converted to a numerical form
        y_train_ohe = to_categorical(y_train)

        # Compile and train the model
        self.model.compile(optimizer='adam',
                            loss='categorical_crossentropy', metrics=["accuracy"])
        self.model.fit(X_train, y_train_ohe, epochs=epochs,
                       batch_size=batch_size, verbose=0)

    def evaluate_model(self, X_test, y_test):
        # Categorical data must be converted to a numerical form
        y_test_ohe = to_categorical(y_test)

        # Evaluate the model
        loss, accuracy = self.model.evaluate(
            X_test, y_test_ohe, verbose=0)
        return accuracy

    def main(self):
        try:
            X, y = self.load_data()

            X_train, X_test, y_train, y_test = self.split_data(X, y)

            self.model = self.create_model(
                input_shape=(X.shape[1],), num_classes=len(np.unique(y)))

            self.train_model(X_train, y_train)

            accuracy = self.evaluate_model(X_test, y_test)
            return accuracy

        except Exception as e:
            raise RuntimeError(
                "An exception occurred during model training and evaluation.") from e
