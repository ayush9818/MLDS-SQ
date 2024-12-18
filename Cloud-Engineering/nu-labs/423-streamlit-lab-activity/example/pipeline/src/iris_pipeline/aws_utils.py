from pathlib import Path
import logging

import boto3

logger = logging.getLogger(__name__)


def download_s3(bucket_name: str, object_key: str, local_file_path: Path):
    s3 = boto3.client("s3")
    print(f"Fetching Key: {object_key} from S3 Bucket: {bucket_name}")
    s3.download_file(bucket_name, object_key, str(local_file_path))
    logger.info("File downloaded successfully to %s", local_file_path)


def upload_files_to_s3(bucket_name: str, prefix: str, directory: Path) -> bool:
    # Check for AWS credentials
    try:
        session = boto3.Session()
        s3 = session.client("s3")
    except Exception as e:
        logger.error("Failed to create boto3 session: %s", e)
        return False

    # Check if bucket exists
    try:
        s3.head_bucket(Bucket=bucket_name)
    except Exception as e:
        logger.error(
            "The bucket '%s' does not exist or you do not have permission to access it",
            bucket_name,
        )
        logger.error(e)
        return False

    # Iterate through files in directory and upload to S3
    for file_path in directory.glob("*"):
        if file_path.is_file():
            try:
                key = str(
                    Path(prefix) / Path(file_path.name)
                )  # Use prefix instead of file parent
                with file_path.open("rb") as data:
                    s3.upload_fileobj(data, bucket_name, key)
                logger.debug(
                    "File '%s' uploaded to S3 bucket '%s'", file_path.name, bucket_name
                )
            except Exception as e:
                logger.error("Failed to upload file '%s': %s", file_path.name, e)
                return False

    return True
