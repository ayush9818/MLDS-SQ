import os
import csv

import boto3

session = boto3.Session()
s3 = session.client("s3")

bucket_name = os.getenv("BUCKET_NAME", "smf2659-test-0")
file_name = "data.csv"

data = [
    ["name", "favorite_food", "favorite_color"],
    ["Michael", "burrito", "green"],
    ["Kiana", "cookie", "blue"],
]

print(f"Creating {file_name} with {len(data)} rows")
with open(file_name, "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Upload the file to S3
print(f"Uploading {file_name} to s3://{bucket_name}/{file_name}")
s3.upload_file(Filename=file_name, Bucket=bucket_name, Key=file_name)

# Download the file from S3
print(f"Downloading s3://{bucket_name}/{file_name} to downloaded-file.csv")
s3.download_file(Bucket=bucket_name, Key=file_name, Filename="downloaded-file.csv")
