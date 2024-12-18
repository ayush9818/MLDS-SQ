import os
import logging
import boto3

# Setup logging
logger = logging.getLogger("cloudlogger." + __name__)


class S3Handler:
    """Handles s3 upload requests"""

    def __init__(self, aws_config, root_directory_name):
        """
        Initializes the S3Handler with specified AWS bucket configuration
        and includes the root directory name in the prefix.

        Args:
            aws_config (dict): Configuration containing "bucket_name" and "bucket_prefix".
            root_directory_name (str): The top-level directory name to be included in the S3 path.
        """
        self.bucket_name = aws_config["bucket_name"]
        self.bucket_prefix = os.path.join(aws_config["prefix"], root_directory_name)
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_artifacts(self, local_directory):
        """
        Uploads a directory to an S3 bucket, preserving the folder structure.

        Args:
            local_directory (str): The local directory path to upload.
        """
        for root, _, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(self.bucket_prefix, relative_path).replace(
                    "\\", "/"
                )
                logger.info(
                    "Uploading %s to %s/%s...", local_path, self.bucket_name, s3_path
                )
                self.client.upload_file(local_path, self.bucket_name, s3_path)
