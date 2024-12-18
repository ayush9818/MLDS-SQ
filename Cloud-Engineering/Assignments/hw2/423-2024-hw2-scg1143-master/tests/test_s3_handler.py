import pytest
from moto import mock_aws
import boto3
from src.s3_handler import S3Handler


def test_upload_artifacts_success(tmp_path):
    """Test that all files are uploaded successfully to S3."""
    # Setup
    with mock_aws():
        boto3.client("s3").create_bucket(Bucket="test-bucket")
        local_directory = tmp_path / "test_dir"
        local_directory.mkdir()
        (local_directory / "file.txt").write_text("content")

        # Execute
        aws_config = {"bucket_name": "test-bucket", "prefix": "test-prefix"}
        s3_handler = S3Handler(aws_config, "root-directory")
        s3_handler.upload_artifacts(str(local_directory))

        # Verify
        s3_client = boto3.client("s3")
        response = s3_client.list_objects(Bucket="test-bucket")
        assert len(response["Contents"]) == 1
        assert response["Contents"][0]["Key"] == "test-prefix/root-directory/file.txt"


def test_upload_artifacts_permission_error(tmp_path):
    """Test handling of permission errors during upload."""
    # Setup
    with mock_aws():
        local_directory = tmp_path / "test_dir"
        local_directory.mkdir()
        (local_directory / "file.txt").write_text("content")

        # Execute
        aws_config = {"bucket_name": "non-existent-bucket", "prefix": "test-prefix"}
        s3_handler = S3Handler(aws_config, "root-directory")
        # Verify
        with pytest.raises(boto3.exceptions.S3UploadFailedError):
            s3_handler.upload_artifacts(str(local_directory))
