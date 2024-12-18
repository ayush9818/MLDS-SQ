# AWS CLI

The AWS Command Line Interface (CLI) is a tool for interacting with AWS Resources via your command line. The tool is very powerful, but we are only introducing it today to enable a simple `docker login` command for AWS ECR.

## Install

Follow the steps here to [install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) on whichever platform you're using (MacOS, Windows, etc.).

Verify that your installation has succeeded by running:

```shell
which aws
# /usr/local/bin/aws 
aws --version
# aws-cli/2.4.5 Python/3.8.8 Darwin/18.7.0 botocore/2.4.5
```

## Configure

The AWS CLI will need to be configured with credentials in order to run commands against resources in your account. This can be done very simply via the following:

```shell
aws configure
```

Provide the requested information (if you have lost your **Access Key ID** and **Secret Access Key**, new ones can be generated in the **Security credentials** page in your account). For more guidance, see the [AWS CLI - Quick Setup](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html#getting-started-quickstart-new) docs.
