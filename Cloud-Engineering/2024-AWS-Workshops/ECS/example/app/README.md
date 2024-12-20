# Iris Inference

This is a simple [FastAPI](https://fastapi.tiangolo.com/) application that loads a trained machine learning classifier on the [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris) using `scikit-learn` from disk, and provides an endpoint for performing inference on new data.

## Usage

To use this application, you can run the `app.py` script, which will start the FastAPI server.

```bash
python src/app.py
```

This requires an active python environment with the appropriate dependencies installed. It is recommended you do this in a virtual environment for the application. This project uses Poetry for environment management, but also includes a `requirements.txt` file for compatibility with any environment management tool.

By default, the script loads the classifier and preprocessed data from the `model.joblib` and `iris.joblib` files in the same directory as the application. You can modify these files to use your own data.

Once the server is running, you can access the Swagger UI by visiting `http://localhost:8000/docs` in your web browser. From there, you can test the `POST /predict` endpoint by providing a JSON payload with the `sepal_length`, `sepal_width`, `petal_length`, and `petal_width` fields.

## Docker

To run the FastAPI application in a Docker container, you can use the following commands:

```bash
docker build -t iris-inference .
docker run -d --name iris-inference -p 80:80 -v $(pwd)/../pipeline/artifacts:/app/artifacts iris-inference
```

This will build a Docker image for the FastAPI application, and then run a container based on that image. The container will load the trained classifier and preprocessed data from the `model.joblib` and `iris.joblib` files in the `/app` directory, and expose the application on port `80`. The `-v` flag is used to mount the `/path/to/models` directory from the host machine to the `/app` directory inside the container, allowing the FastAPI application to access the model files generated by the pipeline.
