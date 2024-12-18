import boto3

session = boto3.Session()
sts = session.client("sts")
print(sts.get_caller_identity())

