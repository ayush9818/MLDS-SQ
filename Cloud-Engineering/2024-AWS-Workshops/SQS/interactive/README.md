# Running the Example

The included application ([main.py](./main.py)) features a simple python script for sending messages to an SQS queue using the `boto3` library. The application requires active AWS credentials to run as well as an environment variable `QUEUE_URL` with the url of your configured SQS queue.

The application uses `argparse` to allow users to specify one of two commands (`send` or `receive`). When using the `send` command, you can provide the `--message` option to specify a sting of text to use in the message body.

## Setting up

First, you will need to complete the [SQS Activity](../README.md) and have obtain the **Queue URL** from your Queue's information page. Then, make sure you have active credentials in a command line session.

```shell
export QUEUE_URL=<YOUR_QUEUE_URL>
export AWS_PROFILE=personal-sso-admin
aws sso login
aws sts get-caller-identity
```

## Running Locally

Set up a virtual environment

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Now we can run the application with the `send` command to send a message to the queue.

```shell
python main.py send --message "Cool message sent from python!"
```

You could check that this message is in the queue by visiting the SQS dashboard in the AWS Console, or you can run the application again with the `receive` command.

```shell
python main.py receive
```

## Building Image

You can also use the included [Dockerfile](./Dockerfile) to build a docker image that runs the example application.

```shell
docker build -t  sqs-example .
```

## Running Container

When we run the container we will need to inject our credentials as well as the required `QUEUE_URL` environment variable. The following command assumes that you have set both `AWS_PROFILE` and `QUEUE_URL` as done in the [Setting up](#setting-up) step above. Both of these variables are passed through to the docker container.

```shell
docker run \
    -v ~/.aws:/root/.aws \
    -e AWS_PROFILE \
    -e QUEUE_URL \
    sqs-example \
    send --message "Cool message sent from Docker"
```

And similarly:

```shell
docker run \
    -v ~/.aws:/root/.aws \
    -e AWS_PROFILE \
    -e QUEUE_URL \
    sqs-example \
    receive
```
