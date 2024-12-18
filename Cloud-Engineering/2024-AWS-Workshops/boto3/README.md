# Boto3

The Boto3 library provides a complete SDK for working with AWS resources. This includes both management and consumer type tasks (e.g. creating and configuring an S3 bucket as well as interacting with that bucket by uploading/downloading content).

Over time, this document may expand to cover common boto3 use-cases and designs, but for now we will focus on credentials.

## Authenticating from Boto3

There are quite a few ways authenticate your application to work with an AWS account when using python and `boto3`. This is documented in depth in the [Boto3 Guide - Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

At a high level, there are two types of methods for authorizing your boto3 API calls:

1. Explicit credentials: passed directly to `boto3.client()` or `boto3.Session()` in your python code.
2. Default credential chain: pull credentials from one of the default locations expected by boto3

In general, you will almost always want to use **Default credential chain**; e.g. do *not* set credentials explicitly with your python code. This is to improve the flexibility of your code; users should be able to run your application locally or in production without modifying the code. These different environments often use different AWS accounts and/or different sources for credentials (e.g. `~/.aws/credentials` file, environment variables, or a Role assigned directly to the EC2 Instance or Lambda Function).

> One exception to this generalization is if your application concurrently deals with several boto3 sessions, each using different identities/credentials.

### Credential Chain

The "credential chain" is just the order in which boto3 will look for credentials when making API calls. The default order looks like the following:

1. Passing credentials as parameters in the boto.client() method
2. Passing credentials as parameters when creating a Session object
3. Environment variables
4. Shared credential file (~/.aws/credentials)
5. AWS config file (~/.aws/config)
6. Assume Role provider
7. Boto2 config file (/etc/boto.cfg and ~/.boto)
8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.


## Examples

For all of these examples, we will be using a python application that looks like the following:

```python title=app.py
import boto3

session = boto3.Session()
sts = session.client("sts")
print(sts.get_caller_identity())
```

### Setup

Before we get started, we need to set up our environment. This guide assumes you have installed the `aws` CLI. If you have not yet configured an aws profile, do so with the following:

```shell
aws configure sso --profile personal-sso-admin
```

You may name the profile whatever you like so long as it helps you identify the Account/Role being used. In this guide, we will use `personal-sso-admin`.

If you have already done this, you may need to login to refresh credentials. Once you have done so, verify your identity using `sts`.

```shell
aws sso login --profile personal-sso-admin
aws sts get-caller-identity --profile personal-sso-admin
```

Now we will set up our python environment

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Using a named profile from credentials file (recommended)

The cleanest way to authenticate your boto3 calls is to used the shared credentials file which can be used by any number of applications or libraries. This file has sections for each named profile so you simply need to tell you application which profile to use. Setting the profile can (and **should**) be done with environment variables as seen below:

```shell
export AWS_PROFILE=personal-sso-admin
python app.py
```

### Setting credential environment variables directly

If you need to have your credentials stored in environment variables, you can do so via the following.

> Note: this uses a named profile's credentials to generate `export AWS_*` commands that contain the proper names/values for env vars. You can check the command output yourself, or just set them by evaluating the output directly with the `eval $()` format.

```shell
eval $(aws configure export-credentials --format env --profile personal-sso-admin)
python app.py
```

## Using Docker

Running your application in a Docker container can provide a challenge since the container will not share the files nor environment variables with your local client. However, we can still utilize both of the above methods when we construct our docker **run** command.

> NOTE: For the same reasons we do not inject credentials explicitly into our application (security and flexibility), you should not inject credentials into the built docker image. To put it another way, your `docker build` command (and by extension, your `Dockerfile`) should not have any credentials-related information.

```shell
docker build -t boto3-example .
```

### Using the shared credential file with Docker

Here we must mount the shared credential file to our container, as well as tell it which section (named profile) to use. This is the simplest way to authorize your boto3 calls from the Docker container.

```shell
docker run -v ~/.aws:/root/.aws -e AWS_PROFILE=personal-sso-admin boto3-example
```

### Using credential environment variables with Docker

Instead of mounting a file, we can directly inject the specific credentials we want docker to use as environment variables. In some cases, this may be preferred since it keeps the container more isolated.

```shell
eval $(aws configure export-credentials --format env --profile personal-sso-admin)
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN boto3-example
```
