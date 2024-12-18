import numpy as np
import mlflow
from mlflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from mlflow.models import infer_signature
import matplotlib.pyplot as plt

# Define constants
EPOCHS = 3
BATCH_SIZE = 1000

def load_data():
    # Load the MNIST dataset
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    # Preprocess the data
    train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
    test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)
    
    return train_images, train_labels, test_images, test_labels

def create_model():
    # Define the model architecture
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

def train_model(model, train_images, train_labels, test_images, test_labels):
    # Train the model
    history = model.fit(train_images, train_labels, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_data=(test_images, test_labels))
    
    return history

def evaluate_model(model, test_images, test_labels):
    # Evaluate the model
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test accuracy:', test_acc)
    
    return test_loss, test_acc

def plot_training_history(history):
    # Plot training history
    history_dict = history.history
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    acc_values = history_dict['accuracy']
    val_acc_values = history_dict['val_accuracy']

    epochs = range(1, len(loss_values) + 1)

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, loss_values, 'bo', label='Training loss')
    plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, acc_values, 'bo', label='Training accuracy')
    plt.plot(epochs, val_acc_values, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()

if __name__ == "__main__":
    # Set MLflow tracking URI (optional)
    # mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

    # Create a new MLflow Experiment
    mlflow.set_experiment("MLflow Keras MNIST")

    mlflow.autolog()

    # Load data
    train_images, train_labels, test_images, test_labels = load_data()
    
    # Create model
    model = create_model()

    # Start MLflow run
    with mlflow.start_run() as run:
        # Train the model
        print("Training Model..")
        history = train_model(model, train_images, train_labels, test_images, test_labels)
        
        # Evaluate the model
        print("Evaluating Model..")
        test_loss, test_acc = evaluate_model(model, test_images, test_labels)
        
        # Plot and save training history plot
        plot_training_history(history)
        plt.savefig("training_history.png")
        
        # Log model and metrics to MLflow
        print("Logging Model..")
        mlflow.keras.log_model(model, "model")
        mlflow.log_metric("test_loss", test_loss)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_artifact("training_history.png", "plots")

        params = {"optimizer": "Adam"}

        # Infer the model signature
        y_pred = model.predict(train_images)
        signature = infer_signature(train_images, y_pred)

        # Log parameters and metrics using the MLflow APIs
        mlflow.log_params(params)

        print("Registering Model..")
        # Log the keras model and register as version 1
        mlflow.keras.log_model(
            model=model,
            artifact_path="keras-model",
            signature=signature,
            registered_model_name="keras-mnist-model",
        )
