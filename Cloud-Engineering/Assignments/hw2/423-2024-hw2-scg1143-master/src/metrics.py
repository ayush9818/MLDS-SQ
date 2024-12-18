import logging
import os
from collections import defaultdict
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)

logger = logging.getLogger("cloudlogger." + __name__)


class EvaluationMetrics:
    """
    A class for scoring machine learning models based on configurable metrics.

    Attributes:
        config (dict): Configuration for the scoring metrics.
    """

    def __init__(self, config):
        """
        Initializes the ScoringMetrics class with a specific configuration.

        Args:
            config (dict): A dictionary containing a list of metrics to score.
        """
        self.config = config

    def evaluate_performance(self, scores):
        """
        Scores a model based on the metrics specified in the config.

        Args:
            model: A trained machine learning model.
            data (tuple): A tuple containing features (X) and target (y) as numpy arrays.

        Returns:
            pd.DataFrame: A DataFrame containing the scores for each metric.
        """
        y_true = scores["y_true"]
        y_pred = scores["y_pred"]
        y_proba = scores.get("y_prob", None)
        metrics_dict = defaultdict(pd.DataFrame)
        eval_metrics = self.calculate_metrics(y_true, y_pred, y_proba)
        metric_df = pd.DataFrame([eval_metrics])
        logger.info("Model scored. Scores: %s", eval_metrics)
        metrics_dict["eval_metrics"] = metric_df
        self.generate_reports(y_true, y_pred, metrics_dict)
        return metrics_dict

    def calculate_metrics(self, y_true, y_pred, y_proba):
        """
        Calculates and returns a dictionary of evaluation metrics specified in the config.

        Args:
            y_true (array-like): True labels of the data.
            y_pred (array-like): Predicted labels by the model.
            y_proba (array-like, optional): Probabilities of the predictions, needed for AUC ROC.

        Returns:
            dict: Metrics calculated as per the config.
        """
        eval_metrics = {}
        for metric in self.config["metrics"]:
            if metric == "accuracy_score":
                score = accuracy_score(y_true, y_pred)
                eval_metrics["Accuracy"] = score
            elif metric == "f1_score":
                score = f1_score(y_true, y_pred, average="macro")
                eval_metrics["F1 Score"] = score
            elif metric == "precision_score":
                score = precision_score(y_true, y_pred, average="macro")
                eval_metrics["Precision"] = score
            elif metric == "recall_score":
                score = recall_score(y_true, y_pred, average="macro")
                eval_metrics["Recall"] = score
            elif metric == "auc_roc_score" and y_proba is not None:
                score = roc_auc_score(y_true, y_proba)
                eval_metrics["AUC ROC"] = score
            else:
                logger.error("Unknown metric %s. Skipping", metric)
        return eval_metrics

    def generate_reports(self, y_true, y_pred, metrics_dict):
        """
        Generates and adds classification report and confusion matrix to the metrics_dict.

        Args:
            y_true (array-like): True labels of the data.
            y_pred (array-like): Predicted labels by the model.
            metrics_dict (dict): Dictionary to store the generated reports.
        """
        for report_name in self.config["reports"]:
            if report_name == "classification_report":
                cr = classification_report(y_true, y_pred, output_dict=True)
                cr = pd.DataFrame(cr).transpose()
                metrics_dict["classification_report"] = cr
            elif report_name == "confusion_matrix":
                cm = confusion_matrix(y_true, y_pred)
                cm = pd.DataFrame(
                    cm,
                    index=["Actual negative", "Actual positive"],
                    columns=["Predicted negative", "Predicted positive"],
                )
                metrics_dict["confusion_matrix"] = cm
            else:
                logger.error("Unknown report type: %s. Skipping", report_name)

    def save_metrics(self, metrics_dict, metrics_dir):
        """
        Saves each metric in the provided dictionary as a CSV file within the specified directory.

        This method creates the directory if it does not already exist and then iterates through
        the dictionary of metrics. Each metric DataFrame is saved as a CSV file named after the metric.

        Args:
            metrics_dict (dict): A dictionary where keys are metric names and values are Pandas DataFrames
                                containing the metric data.
            metrics_dir (str or Path): The directory path where the metric CSV files will be saved.
        """
        os.makedirs(metrics_dir, exist_ok=True)

        for metric_name, metric_df in metrics_dict.items():
            metric_df.to_csv(metrics_dir / f"{metric_name}.csv", index=True)
            logger.info("Saved %s metrics to %s", metric_name, metrics_dir)
