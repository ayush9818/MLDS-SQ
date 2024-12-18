import streamlit as st
import pandas as pd
import numpy as np
import logging
from tensorflow.keras.models import load_model

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load the model
def load_model(model_path):
    try:
        model = load_model(model_path)
        return model
    except Exception as e:
        logging.error(f"Error loading prediction model: {str(e)}")

# Predict the species for input data
def predict(input_data, model, species):
    try:
        predictions = model.predict(input_data)
        predicted_species = [species[np.argmax(prediction)] for prediction in predictions]
        return predicted_species
    except Exception as e:
        logging.error(f"Error predicting species: {str(e)}")

def run_app():
    st.title('Iris Flower Prediction')
    st.header('App3')

    # Load prediction models
    model_paths = {
        'Model A': '../../models/iris_model_a.h5',
        'Model B': '../../models/iris_model_b.h5'
    }
    model_name = st.sidebar.selectbox('Select Model', list(model_paths.keys()))
    model_path = model_paths[model_name]
    model = load_model(model_path)

    if model is not None:
        # Input text boxes for feature values
        sepal_length = st.text_input('Sepal Length (cm):')
        sepal_width = st.text_input('Sepal Width (cm):')
        petal_length = st.text_input('Petal Length (cm):')
        petal_width = st.text_input('Petal Width (cm):')

        # Convert input values to floats
        try:
            sepal_length = float(sepal_length)
            sepal_width = float(sepal_width)
            petal_length = float(petal_length)
            petal_width = float(petal_width)
            logging.info(f'User input: {sepal_length},{sepal_width},{petal_length},{petal_width}')
           
        except ValueError:
            st.write('Please enter numerical values for all features.')
            st.stop()

        # Create a dataframe with the input values
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        # Define the flower species
        species = ['Setosa', 'Versicolor', 'Virginica']

        # Predict species
        predicted_species = predict_species(input_data, model, species)

        if predicted_species is not None:
            logging.info(f'Predicted Species: {predicted_species[0]}')
            # Display the predicted species
            st.subheader('Prediction:')
            st.write(predicted_species[0])


# Run the Streamlit app
if __name__ == '__main__':
    run_app()