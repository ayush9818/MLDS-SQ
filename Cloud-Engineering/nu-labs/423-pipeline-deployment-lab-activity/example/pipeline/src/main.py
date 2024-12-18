import json
import os
import re
from pathlib import Path
import logging
from time import sleep

import typer
import botocore
import joblib
import yaml
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

import aws_utils as aws

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


artifacts = Path() / "artifacts"

ARTIFACTS_PREFIX = os.getenv("ARTIFACTS_PREFIX", "artifacts/")
BUCKET_NAME = os.environ["BUCKET_NAME"]

MODELS = {
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "RandomForestClassifier": RandomForestClassifier,
}


def load_config(config_ref: str) -> dict:
    if config_ref.startswith("s3://"):
        # Get config file from S3
        config_file = Path("config/downloaded-config.yaml")
        try:
            bucket, key = re.match(r"s3://([^/]+)/(.+)", config_ref).groups()
            aws.download_s3(bucket, key, config_file)
        except AttributeError:  # If re.match() does not return groups
            logger.error("Could not parse S3 URI: %s", config_ref)
            config_file = Path("config/default.yaml")
        except botocore.exceptions.ClientError as e:  # If there is an error downloading
            logger.error("Unable to download config file from S3: %s", config_ref)
            logger.error(e)
    else:
        # Load config from local path
        config_file = Path(config_ref)
    if not config_file.exists():
        raise EnvironmentError(f"Config file at {config_file.absolute()} does not exist")

    with config_file.open() as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


def run_pipeline(config):
    """Run the pipeline to produce a classifier model for the Iris dataset"""
    # Load the Iris dataset
    iris = load_iris(return_X_y=False)

    run_config = config.get("run_config", {})
    logger.info("Run Config: %s", run_config)
    version = run_config.get("version", "default")
    run_output = artifacts / version
    run_output.mkdir(parents=True, exist_ok=True)
    logger.info("Saving artifacts to %s", run_output.absolute())

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, **config.get("train_test_split", {})
    )

    # Get config sections; default to empty dict if section is missing
    model_config = config.get("model", {})

    # Create a decision tree classifier
    model = MODELS[model_config.get("type", "DecisionTreeClassifier")]
    clf = model(**model_config.get("params", {}))

    # Train the classifier on the training set
    clf.fit(X_train, y_train)

    # Evaluate the classifier on the test set
    score = clf.score(X_test, y_test)
    logger.info(f"Classifier accuracy: {score:.2f}")

    # Save the data and model to the file system
    joblib.dump(iris, run_output / "iris.joblib")
    joblib.dump(clf, run_output / "iris_classifier.joblib")

    run_prefix = str(run_output) + "/"
    aws.upload_files_to_s3(BUCKET_NAME, run_prefix, run_output)


def process_message(msg: aws.Message):
    message_body = json.loads(msg.body)
    bucket_name = message_body["detail"]["bucket"]["name"]
    object_key = message_body["detail"]["object"]["key"]
    config_uri = f"s3://{bucket_name}/{object_key}"
    logger.info("Running pipeline with config from: %s", config_uri)
    config = load_config(config_uri)
    run_pipeline(config)


def main(
    sqs_queue_url: str,
    max_empty_receives: int = 3,
    delay_seconds: int = 10,
    wait_time_seconds: int = 10,
):
    # Keep track of the number of times we ask queue for messages but receive none
    empty_receives = 0
    # After so many empty receives, we will stop processing and await the next trigger
    while empty_receives < max_empty_receives:
        logger.info("Polling queue for messages...")
        messages = aws.get_messages(
            sqs_queue_url,
            max_messages=2,
            wait_time_seconds=wait_time_seconds,
        )
        logger.info("Received %d messages from queue", len(messages))

        if len(messages) == 0:
            # Increment our empty receive count by one if no messages come back
            empty_receives += 1
            sleep(delay_seconds)
            continue

        # Reset empty receive count if we get messages back
        empty_receives = 0
        for m in messages:
            # Perform work based on message content
            try:
                process_message(m)
            # We want to suppress all errors so that we can continue processing next message
            except Exception as e:
                logger.error("Unable to process message, continuing...")
                logger.error(e)
                continue
            # We must explicitly delete the message after processing it
            aws.delete_message(sqs_queue_url, m.handle)
        # Pause before asking the queue for more messages
        sleep(delay_seconds)


if __name__ == "__main__":
    typer.run(main)
