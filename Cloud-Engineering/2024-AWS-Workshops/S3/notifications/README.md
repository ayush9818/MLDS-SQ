# S3 Event Notifications

This tutorial assumes completion of both the [S3 Tutorial](../README.md) as well as the [SQS Tutorial](../../SQS/README.md).

Oftentimes we want to be notified of activity in an S3 bucket. This may include new files being uploaded, files being deleted, or configuration changes on the bucket itself. All of these activities are captured as "Events" and we can produce "Notifications" for them in a configurable and consumable way. This is one of the key enablers of "event-driven architectures".

There are two main ways to enable notifications for events in S3: Direct S3 Event Notification Configurations and EventBridge Rules. We will cover both in this tutorial, but EventBridge is the newer way to accomplish this and is a much more flexible and scalable method.

## Direct S3 Event Notification

S3 includes quite a few guides and tutorials on configuring event notifications; you can refer to them as needed.

[S3 User Guide - Ways to add notification config to bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html)

---

First, create a bucket if you do not have one that you can use for this tutorial, then, visit the **Properties** tab from the bucket's dashboard page.

![S3 Notifications bucket](images/s3-notif-00-bucket.png)

---

Scroll down to the **Event notifications** section and **Create event notification**.

![S3 Notifications notifications](images/s3-notif-01-notifications.png)

---

Give the configuration a name and select the events that you are interested in (we will just use object create events for now).

![S3 Notifications create-notif](images/s3-notif-02-create-notif.png)

---

Now we set the target for our notifications to be the SQS Queue we created during the [SQS Tutorial](../../SQS/README.md).

If you try and save the configuration you will get an error that the configuration failed. This is because we have not yet configured the access policy on our target queue. The info box above tells us how to resolve this.

![S3 Notifications target-failed](images/s3-notif-03-target-failed.png)

---

Visit the SQS queue that you created in the Console and edit its access policy.

![S3 Notifications queue-edit-policy](images/s3-notif-04-queue-edit-policy.png)

---

To come up with this policy, we will follow the guidance in [S3 User Guide - Grand destination permissions to S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/grant-destinations-permissions-to-s3.html#sqs-queue-policy).

In short, you will add an additional statement to your queue's access policy that looks like the following:

> Note, you will have to swap in your own queue ARN, bucket name, and account ID.

```json
        {
            "Sid": "allow-s3-events",
            "Effect": "Allow",
            "Principal": {
                "Service": "s3.amazonaws.com"
            },
            "Action": [
                "SQS:SendMessage"
            ],
            "Resource": "<your-sqs-queue-arn>",
            "Condition": {
                "ArnLike": {
                    "aws:SourceArn": "arn:aws:s3:*:*:<your-s3-bucket-name>"
                },
                "StringEquals": {
                    "aws:SourceAccount": "<your-account-id>"
                }
            }
        }
```

<details>
    <summary>Example of a complete policy statement for my account</summary>

```json
{
  "Version": "2012-10-17",
  "Id": "__default_policy_ID",
  "Statement": [
    {
      "Sid": "__owner_statement",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::546734626740:root"
      },
      "Action": "SQS:*",
      "Resource": "arn:aws:sqs:us-east-2:546734626740:mlds-sqs-workshop"
    },
    {
      "Sid": "allow-s3-events",
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": ["SQS:SendMessage"],
      "Resource": "arn:aws:sqs:us-east-2:546734626740:mlds-sqs-workshop",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:smf2659-sqs-workshop"
        },
        "StringEquals": {
          "aws:SourceAccount": "546734626740"
        }
      }
    }
  ]
}
```

</details><br>

Once the policy is in place, click **Save**.

![S3 Notifications queue-update-policy](images/s3-notif-05-queue-update-policy.png)

---

Return to the tab with the in-progress S3 event notification configuration, and save it. You should see a confirmation like the following

![S3 Notifications save-notif-config](images/s3-notif-06-save-notif-config.png)

---

Now upload a file to the bucket (like the included [data.json](./data.json))

![S3 Notifications upload-object](images/s3-notif-xx-upload-object.png)

---

Then, return to the queue's dashboard to poll for messages again.

![Receive messages](../../SQS/images/sqs-06-receive-test-msg.png)

---

You should see a message like the following which captures the S3 event.

![S3 Notifications queue-msg](images/s3-notif-07-queue-msg.png)

The full message body can be seen in [s3-event-notification-message.json](./s3-event-notification-message.json).

---

Now, let's clean up by deleting the message...

![S3 Notifications queue-delete-msg](images/s3-notif-08-queue-delete-msg.png)

---

and the event notification configuration as well. We will add an Event Bridge notification next! Click on the **Edit** button for **Amazon EventBridge**.

![S3 Notifications delete-notif-config](images/s3-notif-09-delete-notif-config.png)

---

## Using EventBridge Notifications (new/preferred method)

EventBridge is a very powerful and flexible service that allows you to consume events from all sorts of services in AWS as well as produce your own custom events. You can read more about it in the [AWS EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html). In this tutorial, we will just scratch the surface by enabling S3 events and setting up a rule to match object creation events in a specific bucket.

We will be configuring an EventBridge rule similar to what is done in [EventBridge User Guide - S3 Object Created](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-s3-object-created-tutorial.html); except we will use SQS as a target instead of SNS.

---

The only change you need to make to S3 is to simply enable Amazon EventBridge notifications and **Save changes**.

![S3 Notifications enable-eventbridge](images/s3-notif-10-enable-eventbridge.png)

---

Now, head over to the [EventBridge Dashboard](https://us-east-2.console.aws.amazon.com/events/home?region=us-east-2#/), and click **Create rule**.

![S3 Notifications eb-dashboard](images/s3-notif-11-eb-dashboard.png)

---

Give the rule a name and description and continue on by clicking **Next**.

![S3 Notifications eb-rule-create](images/s3-notif-12-eb-rule-create.png)

---

Choose **AWS events** as the source and optionally set the Sample event to **Object Created** for testing purposes.

![S3 Notifications eb-rule-source](images/s3-notif-13-eb-rule-source.png)

---

Now, specify a rule pattern by selecting S3 as the Event source, Event Notification as the Event type, Object Created as the Specific event, and the name of your bucket as the specific bucket.

![S3 Notifications eb-rule-pattern](images/s3-notif-14-eb-rule-pattern.png)

> Note, if you test the event at this point, it will fail because the sample event is for a bucket named "example-bucket", you will need to change it as follows
> 
---

We will modify the sample event to match our custom event rule since the sample event comes from a bucket named "example-bucket". Copy the starter event from the Sample Event box, and then change the sample event to "**Enter my own**".

![S3 Notifications sample-event-starter](images/s3-notif-15-sample-event-starter.png)

---

Paste the sample event and then change the bucket name to the name of your bucket.

![S3 Notifications sample-event-custom](images/s3-notif-16-sample-event-custom.png)

---

Now you can test the event to ensure the pattern matches. Then proceed with the creation.

![S3 Notifications test-event](images/s3-notif-17-test-event.png)

---

We set the target for this event to be SQS and select our created queue from the dropdown.

![S3 Notifications target](images/s3-notif-18-target.png)

---

Review your configuration and continue to **Create rule**.

![S3 Notifications review-confirm](images/s3-notif-19-review-confirm.png)

---

You should see a confirmation like the following:

![S3 Notifications rule-created](images/s3-notif-20-rule-created.png)

---

Now, head back over to your SQS queue's dashboard and see how the Access policy has been modified by EventBridge to add the required permission for you. How convenient!

![S3 Notifications sqs-policy-updated](images/s3-notif-21-sqs-policy-updated.png)

---

Go back to your S3 bucket and delete the previously uploaded file (since we will want to re-upload it now to test our new notifications).

![S3 Notifications delete-object](images/s3-notif-22-delete-object.png)

---

Now upload the file to the bucket again.

![S3 Notifications upload-object](images/s3-notif-xx-upload-object.png)

---

Go back to your queue dashboard and check for new messages.

![S3 Notifications queue](images/s3-notif-23-queue.png)

---

Poll for messages.

![S3 Notifications queue-receive](images/s3-notif-24-queue-receive.png)

---

You should see a single message again for the new object notification.

> Note: you may actually see multiple messages here; EventBridge usually sends a test event to verify proper configuration and permission to deliver messages. You may also see multiple messages if you failed to delete the previously configured S3 Event Notification Configuration.

![S3 Notifications queue-msgs](images/s3-notif-25-queue-msgs.png)

---

Inspect the message to see a record like the following:

![S3 Notifications eb-msg-body](images/s3-notif-26-eb-msg-body.png)

The full message body content can be seen in [event-bridge-message.json](./event-bridge-message.json)

---

## Example Commands

We used the console above, but we can also test this out from the command line.

```shell
QUEUE_URL=https://sqs.us-east-2.amazonaws.com/546734626740/mlds-sqs-workshop
BUCKET_NAME=smf2659-sqs-workshop

aws s3 cp ./data.json s3://$BUCKET_NAME/

aws sqs receive-message --queue-url $QUEUE_URL --max-number-of-messages 1 > message.json
cat message.json | jq
cat message.json | jq -r '.Messages[0].Body' | jq

HANDLE=$(cat message.json | jq -r '.Messages[0].ReceiptHandle')
aws sqs delete-message --queue-url $QUEUE_URL --receipt-handle $HANDLE
```
