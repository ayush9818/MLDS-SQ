from pathlib import Path
import logging
from dataclasses import dataclass

import boto3
import botocore.exceptions

logger = logging.getLogger(__name__)


def download_s3(bucket_name: str, object_key: str, local_file_path: Path):
    s3 = boto3.client("s3")
    logger.debug("Fetching Key: %s from S3 Bucket: %s", object_key, bucket_name)
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
            "The bucket '%s' does not exist or you do not have permission to access it", bucket_name
        )
        logger.error(e)
        return False

    # Iterate through files in directory and upload to S3
    for file_path in directory.glob("*"):
        if file_path.is_file():
            try:
                key = str(Path(prefix) / Path(file_path.name))  # Use prefix instead of file parent
                logger.info("Uploading file to s3: s3://%s/%s", bucket_name, key)
                with file_path.open("rb") as data:
                    s3.upload_fileobj(data, bucket_name, key)
            except Exception as e:
                logger.error("Failed to upload file '%s': %s", file_path.name, e)
                return False

    return True


@dataclass
class Message:
    handle: str
    body: str


def get_messages(
    queue_url: str,
    max_messages: int = 1,
    wait_time_seconds: int = 1,
) -> list[Message]:
    sqs = boto3.client("sqs")
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
        )
    except botocore.exceptions.ClientError as e:
        logger.error(e)
        return []
    if "Messages" not in response:
        return []
    return [Message(m["ReceiptHandle"], m["Body"]) for m in response["Messages"]]


def delete_message(queue_url: str, receipt_handle: str):
    sqs = boto3.client("sqs")
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
