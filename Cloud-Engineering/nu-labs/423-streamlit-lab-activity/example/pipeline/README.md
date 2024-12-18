# Iris Pipeline

This is a simple machine learning pipeline that trains a classifier on the [Iris dataset](https://archive.ics.uci.edu/ml/datasets/iris) using `scikit-learn`, and saves the trained model to disk as a `joblib` file.

## Usage

This project requires an active python environment with the appropriate dependencies installed. It is recommended you do this in a virtual environment for the application. This project uses Poetry for environment management, but also includes a `requirements.txt` file for compatibility with any environment management tool.

```shell
poetry install
poetry shell

# OR...

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To use this pipeline, you can run the `main.py` script, which will train the classifier and save the model files to disk.

```bash
python src/main.py
```

By default, the script uses the iris.csv dataset file in the same directory as input data. You can modify this file to use your own data. The script outputs two joblib files, `model.joblib` and `iris.joblib`, which contain the trained classifier and preprocessed data respectively.

## Docker

To run the pipeline in a Docker container, you can use the following commands:

```bash
docker build -t iris-pipeline .
docker run -v $(pwd)/artifacts:/app/artifacts iris-pipeline

# OR

docker run -v $(pwd)/../iris_app/artifacts:/app/artifacts iris-pipeline
```

NOTE: for more on using Docker volumes, see: [https://docs.docker.com/storage/volumes/](https://docs.docker.com/storage/volumes/).

This will build a Docker image for the pipeline, and then run a container based on that image. The container will train the classifier and save the model files to disk during startup.
available_models = load_model_versions(artifacts)
