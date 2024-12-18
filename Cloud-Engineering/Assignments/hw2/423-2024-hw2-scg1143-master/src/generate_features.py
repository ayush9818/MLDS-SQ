import logging
import pandas as pd
import numpy as np

# Setup logging
logger = logging.getLogger("cloudlogger." + __name__)


class FeatureGenerator:
    """
    Class to generate new features from existing data.

    Attributes:
        data (pd.DataFrame): The initial dataset for feature generation.
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def calculate_norm_range(self, feature_name: str, params: dict) -> None:
        """Calculates normalized range for specified columns."""
        try:
            min_col = params["min_col"]
            max_col = params["max_col"]
            mean_col = params["mean_col"]
            self.data[feature_name] = (
                self.data[max_col] - self.data[min_col]
            ) / self.data[mean_col]
            logger.info(
                "%s calculated using %s, %s, and %s",
                feature_name,
                min_col,
                max_col,
                mean_col,
            )
        except KeyError as e:
            logger.error("Missing key during norm range calculation: %s", e)
            raise KeyError("Missing key during norm range calculation") from e

    def calculate_range(self, feature_name: str, params: dict) -> None:
        """Calculates range for specified columns."""
        try:
            min_col = params["min_col"]
            max_col = params["max_col"]
            self.data[feature_name] = self.data[max_col] - self.data[min_col]
            logger.info("%s calculated using %s and %s", feature_name, min_col, max_col)
        except KeyError as e:
            logger.error("Missing key during range calculation: %s", e)
            raise KeyError("Missing key during range calculation") from e

    def log_transform(self, feature_name: str, source_col: str) -> None:
        """Applies logarithmic transformation to the specified column."""
        try:
            self.data[feature_name] = self.data[source_col].apply(np.log)
            logger.info("%s log transformation applied on %s", feature_name, source_col)
        except KeyError as e:
            logger.error("Column %s not found in data.", source_col)
            raise KeyError(f"Column {source_col} not found in data.") from e

    def multiply_columns(self, feature_name: str, params: dict) -> None:
        """Multiplies two specified columns to create a new feature."""
        try:
            col_a = params["col_a"]
            col_b = params["col_b"]
            self.data[feature_name] = self.data[col_a] * self.data[col_b]
            logger.info(
                "%s calculated by multiplying %s and %s", feature_name, col_a, col_b
            )
        except KeyError as e:
            logger.error("Missing key during multiplication: %s", e)
            raise KeyError("Missing key during multiplication") from e

    def generate_features(self, feature_config: dict) -> pd.DataFrame:
        """Applies all feature configurations to generate new features."""
        if "calculate_norm_range" in feature_config:
            for feature_name, params in feature_config["calculate_norm_range"].items():
                self.calculate_norm_range(feature_name, params)

        if "calculate_range" in feature_config:
            for feature_name, params in feature_config["calculate_range"].items():
                self.calculate_range(feature_name, params)

        if "log_transform" in feature_config:
            for feature_name, source_col in feature_config["log_transform"].items():
                self.log_transform(feature_name, source_col)

        if "multiply" in feature_config:
            for feature_name, params in feature_config["multiply"].items():
                self.multiply_columns(feature_name, params)
        return self.data
