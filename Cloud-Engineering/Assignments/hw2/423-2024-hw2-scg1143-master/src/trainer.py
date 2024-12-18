import os
import logging
from typing import Any, Dict, Tuple
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression


# Setup logging
logger = logging.getLogger("cloudlogger." + __name__)


SUPPORTED_MODELS = {
    "RandomForestClassifier": RandomForestClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "LogisticRegression": LogisticRegression,
}


class Trainer:
    """Sklearn Model trainer which trains and saves model"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        logger.info("Trainer initialized with configuration.")

    def train_model(self, data: pd.DataFrame) -> Tuple[Any, pd.DataFrame, pd.DataFrame]:
        """
        Trains a model based on the configuration and input data.

        Args:
            data (pd.DataFrame): The dataset to train the model on.

        Returns:
            Tuple[Any, pd.DataFrame, pd.DataFrame]: A tuple containing the trained model, train data, and test data.
        """
        train_config = self.config
        test_size = train_config.get("test_size", 0.25)
        random_state = train_config.get("random_state", 42)
        train_features = train_config.get("train_features", [])
        # Split the data into train and test
        train_data, test_data = train_test_split(
            data, test_size=test_size, random_state=random_state
        )
        logger.info("Data split into train and test sets.")

        # Load the model type from the config
        model_name = train_config.get("model_name")
        model_params = train_config.get("params", {})

        if model_name in SUPPORTED_MODELS:
            model_class = SUPPORTED_MODELS[model_name]
            model = model_class(**model_params)
            model.fit(
                train_data.drop("target", axis=1)[train_features], train_data["target"]
            )
            logger.info("%strained successfully.", model_name)
        else:
            logger.error(
                "Model %sis not supported or not defined in SUPPORTED_MODELS.",
                model_name,
            )
            raise ValueError(f"Model {model_name} is not supported or not defined.")
        return model, train_data, test_data

    def save_data(
        self, train_data: pd.DataFrame, test_data: pd.DataFrame, save_dir: str
    ) -> None:
        """
        Saves the train and test data to the specified directory in CSV format.

        Args:
            train_data (pd.DataFrame): The training data to be saved.
            test_data (pd.DataFrame): The test data to be saved.
            save_dir (str): The directory where data files will be saved.
        """
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        train_path = os.path.join(save_dir, "train_data.csv")
        test_path = os.path.join(save_dir, "test_data.csv")

        train_data.to_csv(train_path, index=False)
        test_data.to_csv(test_path, index=False)
        logger.info("Train data saved to %s", train_path)
        logger.info("Test data saved to %s", test_path)

    def save_model(self, model: Any, file_path: str) -> None:
        """
        Saves the trained model into the specified file_path

        Args:
            model : trained model object
            file_path : path to save the trained model
        """
        parent_dir = file_path.parent
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(file_path, "wb") as f:
            pickle.dump(model, f)
        logger.info("Model saved to %s", file_path)
