import argparse
import os

import boto3

QUEUE_URL = os.environ["QUEUE_URL"]


def send_message(queue_url: str, message_body: str):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message.html
    sqs = boto3.client("sqs")
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    print("Sent message: ", response.get("MessageId"))


def receive_messages(queue_url: str):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/receive_message.html
    sqs = boto3.client("sqs")
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=5)
    messages = response.get("Messages", [])
    for message in messages:
        receipt_handle = message.get("ReceiptHandle")
        body = message.get("Body")
        print("Received message: ", body)
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        print("Deleted message: ", message.get("MessageId"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Send or receive messages to/from an AWS SQS queue"
    )
    parser.add_argument(
        "command", choices=["send", "receive"], help="Whether to send or receive messages"
    )
    parser.add_argument("--message", help="The message to send to the queue")

    args = parser.parse_args()

    if args.command == "send":
        send_message(QUEUE_URL, args.message or "Test message")
    elif args.command == "receive":
        receive_messages(QUEUE_URL)
