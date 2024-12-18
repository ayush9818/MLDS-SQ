import os
import logging
import pandas as pd

# Configure logging
logger = logging.getLogger("cloudlogger." + __name__)


class ModelScorer:
    """
    A class for scoring machine learning models based on specified features
    """

    def __init__(self, config):
        """
        Initializes the ModelScorer class with a specific configuration.

        Args:
            config (dict): A dictionary containing configurations for scoring.
        """
        self.config = config

    def score_model(self, model, data):
        """
        Scores a model based on the configured features and whether probabilities should be included.

        Args:
            model: A trained machine learning model that supports predict and optionally predict_proba.
            data (pd.DataFrame): A DataFrame containing the features and true labels.

        Returns:
            pd.DataFrame: A DataFrame with columns "y_true", "y_pred", and "y_prob" (if probabilities are included).

        Raises:
            AttributeError: If "prob" is True and the model does not support predict_proba.
        """
        # Extract features and true labels
        x = data[self.config["features"]]
        y_true = data["target"]
        # Predict the outcomes
        try:
            y_pred = model.predict(x)
        except AttributeError as e:
            logger.error("Model does not support predict method.")
            raise e

        # Prepare the results DataFrame
        results = {"y_true": y_true, "y_pred": y_pred}
        # Check if probabilities are required
        if self.config.get("prob", False):
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(x)[
                    :, 1
                ]  # Assuming binary classification for simplicity
                results["y_prob"] = y_prob
            else:
                logger.error(
                    "Model does not support predict_proba but prob was set to True."
                )
                raise AttributeError("Model does not support predict_proba method.")

        results_df = pd.DataFrame(results)
        logger.info("Model scored successfully.")

        return results_df

    @staticmethod
    def save_scores(scores, file_path):
        """
        Saves the scores DataFrame to a CSV file at the specified path.

        This method checks if the parent directory of the provided file path exists,
        creates it if it does not, and then saves the DataFrame to a CSV file.

        Args:
            scores (pd.DataFrame): The DataFrame containing scores to be saved.
            file_path (Path): The full path (including filename) where the scores will be saved.
        """
        parent_dir = file_path.parent
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        scores.to_csv(file_path, index=False)
        logger.info("Scores Saved to %s", file_path)
