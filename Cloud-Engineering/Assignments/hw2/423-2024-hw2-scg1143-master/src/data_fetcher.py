import time
import logging
import logging.config
from pathlib import Path
import requests

logger = logging.getLogger("cloudlogger." + __name__)


def get_data(
    url: str, attempts: int = 4, wait: int = 3, wait_multiple: int = 2
) -> bytes:
    """
    Acquires data from URL with retries and increasing wait intervals.

    Args:
        url (str): URL from where data is to be fetched.
        attempts (int): Maximum number of attempts to fetch the data.
        wait (int): Initial wait time between attempts in seconds.
        wait_multiple (int): Factor by which the wait time increases after each failed attempt.

    Returns:
        bytes: The content fetched from the URL.

    Raises:
        RuntimeError: If all attempts to fetch data fail.
    """
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            logger.warning("Attempt %d of %d failed: %s", attempt, attempts, e)
            if attempt == attempts:
                logger.error("All attempts to fetch data have failed.")
                raise RuntimeError(
                    f"Failed to fetch data after {attempts} attempts."
                ) from e
            time.sleep(wait)
            wait *= wait_multiple
    return None


def acquire_data(url: str, save_path: Path) -> None:
    """
    Acquires data from a specified URL and saves it to a local file.

    Args:
        url (str): URL from where data is to be acquired.
        save_path (Path): Local path to write data to.
    """
    url_contents = get_data(url)
    try:
        save_path.write_bytes(url_contents)
        logger.info("Data written to %s", save_path)
    except FileNotFoundError as e:
        logger.error("Please provide a valid file location to save dataset to.")
        raise FileNotFoundError("Invalid file location provided.") from e
    except Exception as e:
        logger.error("Error occurred while trying to write dataset to file: %s", e)
        raise Exception("Error writing dataset to file.") from e
