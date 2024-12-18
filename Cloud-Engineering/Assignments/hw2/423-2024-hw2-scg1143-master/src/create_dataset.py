import logging.config
from pathlib import Path
import pandas as pd
import numpy as np

logger = logging.getLogger("cloudlogger." + __name__)


def create_dataset(raw_data: str, config: dict) -> pd.DataFrame:
    """
    Creates a dataset from raw data based on a configuration.

    Args:
        raw_data (str): The path to the raw data file.
        config (dict): Configuration including column names, and indices for slicing the data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.

    Raises:
        FileNotFoundError: If the raw data file is not found.
        Exception: For other unforeseen errors.
    """
    try:
        # Read data from the specified file
        with open(raw_data, "r") as f:
            data = [
                [s.strip() for s in line.split(" ") if s.strip() != ""]
                for line in f.readlines()
            ]

        # Extract columns from config
        columns = config.get("columns", [])

        if not columns:
            logger.error("Column names are missing in the configuration.")
            raise ValueError("Column names are missing in the configuration.")

        # Prepare data slices based on config, ensuring all needed indices are provided
        processed_data = []
        for class_info in config.get("classes", []):
            start_index = class_info.get("start")
            end_index = class_info.get("end")
            if start_index is None or end_index is None:
                logger.error(
                    "Start or end index missing for a class in the configuration."
                )
                raise ValueError(
                    "Start or end index missing for a class in the configuration."
                )
            class_data = data[start_index:end_index]
            class_data = [
                [float(s.replace("\n", "")) for s in cloud] for cloud in class_data
            ]
            df = pd.DataFrame(class_data, columns=columns)
            df["target"] = np.full(len(df), class_info.get("label", 0))
            processed_data.append(df)

        # Concatenate all class data frames
        full_dataset = pd.concat(processed_data, ignore_index=True)
        logger.info("Dataset successfully created with %d entries", len(full_dataset))
        return full_dataset
    except FileNotFoundError:
        logger.error("The file %s does not exist.", raw_data)
        raise
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise


def save_dataset(data: pd.DataFrame, data_path: Path) -> None:
    """
    Saves the pandas DataFrame to the specified data path in CSV, JSON, or Excel format.

    Args:
        data (pd.DataFrame): The DataFrame to be saved.
        data_path (Path): The file path where the DataFrame should be saved.

    Raises:
        ValueError: If the file extension is not supported.
    """
    try:
        file_extension = data_path.suffix.lower()

        if file_extension == ".csv":
            data.to_csv(data_path, index=False)
            logging.info(f"Dataset successfully saved to {data_path} as CSV.")
        elif file_extension == ".json":
            data.to_json(data_path, orient="records", lines=True)
            logging.info(f"Dataset successfully saved to {data_path} as JSON.")
        elif file_extension == ".xlsx":
            data.to_excel(data_path, index=False)
            logging.info(f"Dataset successfully saved to {data_path} as Excel.")
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    except ValueError as e:
        logging.error(f"Error saving dataset: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving the dataset: {e}")
        raise
