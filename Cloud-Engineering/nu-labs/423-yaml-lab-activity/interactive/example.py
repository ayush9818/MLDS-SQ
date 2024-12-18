import argparse
import logging
from pathlib import Path

import pandas as pd
import yaml  # type: ignore

from src import data_cleaning as dc

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Slice a dataframe according to columns configured"
    )
    parser.add_argument(
        "--config",
        default="config/config.yaml",
        help="path to yaml file with configurations",
    )
    parser.add_argument("--output", default="data/output.csv", help="path to save dataframe")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    data = {
        "name": ["Alice", "Bob", "Carly"],
        "classification": ["Junior", None, "Senior"],
        "grade": [99, 87, None],
    }
    dataframe = pd.DataFrame(data=data)

    # Subset the data
    dataframe = dc.subset_data(dataframe, **config["data_cleaning"]["subset_data"])
    logger.info("DataFrame after subset_data:\n%s", dataframe)

    # Fill missing values
    dataframe = dc.clean_missing(dataframe, **config["data_cleaning"]["clean_missing"])
    logger.info("DataFrame after clean_missing:\n%s", dataframe)

    # Sort the data
    dataframe = dc.reorder(dataframe, **config["data_cleaning"]["reorder"])
    logger.info("DataFrame after reorder:\n%s", dataframe)

    dataframe.to_csv(args.output, index=False)
    logger.info("Output saved to %s", args.output)

    run_config_path = Path(args.output).parent / "run_config.yaml"
    with run_config_path.open("w") as f:
        yaml.dump(config, f)
    logger.info("Run config saved to %s", run_config_path)
