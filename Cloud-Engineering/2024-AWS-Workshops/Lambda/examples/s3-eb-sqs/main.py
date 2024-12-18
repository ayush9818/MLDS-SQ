import json


def lambda_handler(event, context):
    print(event)
    uris = []
    for record in event["Records"]:
        message_body = json.loads(record["body"])
        bucket_name = message_body["detail"]["bucket"]["name"]
        object_key = message_body["detail"]["object"]["key"]
        uris.append(f"s3://{bucket_name}/{object_key}")
        print(f"Object {object_key} created in bucket {bucket_name}.")
        # do something with the object, such as copy it to another S3 bucket or process it

    return {
        "statusCode": 200,
        "body": json.dumps("Successfully processed S3 notifications from EventBridge."),
    }
