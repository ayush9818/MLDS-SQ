import argparse
import datetime
import logging.config
from pathlib import Path
import os
import yaml
from src import data_fetcher as df
from src import create_dataset as cd
from src.generate_features import FeatureGenerator
from src.trainer import Trainer
from src.score_model import ModelScorer
from src.metrics import EvaluationMetrics
from src.s3_handler import S3Handler
from src import eda

logging.config.fileConfig("config/logging/local.ini", disable_existing_loggers=False)
logger = logging.getLogger("cloudlogger." + __name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Acquire, clean, and create features from clouds data"
    )
    parser.add_argument(
        "--config",
        default="config/default-config.yaml",
        help="Path to configuration file",
    )
    args = parser.parse_args()

    # Load configuration file for parameters and run config
    with open(args.config, "r") as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.error.YAMLError as e:
            logger.error("Error while loading configuration from %s", args.config)
        else:
            logger.info("Configuration file loaded from %s", args.config)

    run_config = config.get("run_config", {})

    # Set up output directory for saving artifacts
    now = int(datetime.datetime.now().timestamp())
    artifacts = Path(run_config.get("output_dir", "runs")) / str(now)
    artifacts.mkdir(parents=True)

    # Save config file to artifacts directory for traceability
    with (artifacts / "config.yaml").open("w") as f:
        yaml.dump(config, f)

    # Acquire data from online repository and save to disk
    filename = os.path.basename(run_config["data_source"])
    df.acquire_data(run_config["data_source"], artifacts / filename)

    # # Create structured dataset from raw data; save to disk
    data = cd.create_dataset(artifacts / filename, config["create_dataset"])
    cd.save_dataset(data, artifacts / "clouds.csv")

    # # Enrich dataset with features for model training; save to disk
    gf = FeatureGenerator(data)
    features = gf.generate_features(config["generate_features"])

    # Generate statistics and visualizations for summarizing the data; save to disk
    figures = artifacts / "figures"
    figures.mkdir()
    eda.save_figures(features, figures)

    # # Split data into train/test set and train model based on config; save each to disk
    trainer = Trainer(config["train_config"])
    trained_model, train_data, test_data = trainer.train_model(features)
    trainer.save_data(train_data, test_data, artifacts)
    trainer.save_model(trained_model, artifacts / "trained_model_object.pkl")

    # Score model on test set; save scores to disk
    sm = ModelScorer(config["score_config"])
    scores = sm.score_model(trained_model, test_data)
    sm.save_scores(scores, artifacts / "scores.csv")

    # Evaluate model performance metrics; save metrics to disk
    ep = EvaluationMetrics(config["evaluation_config"])
    metrics = ep.evaluate_performance(scores)
    ep.save_metrics(metrics, artifacts / "metrics")

    # Upload all artifacts to S3
    aws_config = config.get("aws_config")
    if aws_config.get("upload", False):
        s3_handler = S3Handler(aws_config, os.path.basename(artifacts))
        s3_handler.upload_artifacts(artifacts)
