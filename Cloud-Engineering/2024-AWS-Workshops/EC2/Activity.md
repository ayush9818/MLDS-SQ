# EC2 Activity

## Overview

In this tutorial we will perform the following steps:

1. Create a simple, free-tier-eligible EC2 instance
2. Configure that instance with an ssh key and security group
3. Connect to that EC2 instance from our laptop via ssh
4. Create a new IAM Role / EC2 Instance Profile with S3 permissions
5. Use the AWS CLI from the EC2 Instance to interact with S3

> **NOTE**: If you have already completed the [RDS: Free Tier](../RDS/free-tier.md) tutorial which involved deploying an EC2 instance for connecting to your RDS Database, then you will not be able to create a second EC2 Instance for free. The Free Tier only covers a single EC2 Instance and a single Public IPv4 Address allocation. In this case, you may proceed to the ["Connect to Instance"](#connect-to-instance) section in this walkthrough.

## Walkthrough

### Create Instance

Navigate to the EC2 Console ([directly](https://us-east-2.console.aws.amazon.com/ec2/home), or from the [AWS Console dashboard](https://us-east-2.console.aws.amazon.com/console/home))

![service](images/ec2-00-service.png)

From the dashboard, click on "**Launch instance**"

![dashboard](images/ec2-01-dashboard.png)

Now you will walk through the Launch Instance wizard.

Enter a name for your instance like `mlds-ec2-workshop`

Here we will select an "AMI" which will in turn determine the OS that the instance runs. We will use Amazon Linux for this workshop.

![create-instance-name](images/ec2-02-create-instance-name.png)

Next, we select an instance type. For this workshop, make sure you select a `t2.micro` as it is the only free-tier-eligible type (`t3.micro` is also free-tier eligible in _some_ regions).

We now need to select a key pair to use for ssh with the instance. You likely will not have a key pair in your account, so click on "**Create new key pair**".

![create-instance-type](images/ec2-04-create-instance-type.png)

Name your key something useful like `mlds-ec2-workshop`

> NOTE: this file will be be saved to your computer and also kept around in your AWS account so you should take care to name it something meaningful.

You will be prompted to save the private key file to your laptop. **Make sure you save it here as you will not be able to retrieve it later**.

> I tend to keep all of my ssh keys in a single folder where I can find them easily. For me, that is `~/.ssh/keys` (your default ssh key will be kept at `~/.ssh/id_rsa`, the folder `~/.ssh/keys` will not exist by default but you can create it if you like).

![create-instance-keypair](images/ec2-05-create-instance-keypair.png)

Now we assign a security group to the instance. You can easily create a new security group and configure it with a proper inbound rule to allow SSH access.

![create-instance-sg](images/ec2-06-create-instance-sg.png)

Instead of allowing SSH access from anywhere, we are going to create a custom rule to only allow inbound connections that come from the Northwestern IP space.

![create-instance-rule](images/ec2-07-create-instance-rule.png)

Security Group Rules use what is called a "CIDR" block for defning a range of IP Addresses. We are going to use the [IP range for the Northwestern VPN](https://services.northwestern.edu/TDClient/30/Portal/KB/ArticleDet?ID=1920).

Enter `165.124.160.0/21` for the Custom range, and click on the **CIDR block** below.

![create-instance-custom](images/ec2-08-create-instance-custom.png)

We can leave the default storage setting, confirm all configuration, and click "**Launch instance**" when we are ready.

> Note: you can increase the attached storage up to the max Free-Tier-Eligible size of 30 GiB if you would like.

![create-instance-create](images/ec2-09-create-instance-create.png)

### Connect to Instance

After your instance has finished launching, you will see the following page; click "**Connect to Instance**".

![create-instance-complete](images/ec2-10-create-instance-complete.png)

**EC2 Intsance Connect** has probably not been configured in your account so we will connect over SSH. Click on the SSH client tab

![connect-tab](images/ec2-11-connect-tab.png)

This page will give you instructions that can be copy/pasted to connect to your newly deployed instance. Be sure and copy them from *your* dashboard as the following screenshot will not have the right DNS name for your instance.

> NOTE: if you have moved your private key file to some other location, make sure you either `cd` to that location **or** change the commands to point at the proper location of said file.
> E.g. `ssh -i ~/.ssh/keys/mlds-ec2-workshop.pem ec2-user@...`

![connect-ssh](images/ec2-12-connect-ssh.png)

Now, the first time you connect, you will see a message like the following:

```log
The authenticity of host '...' can't be established.
...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

This  will always happen when you connect to a server for the first time. Just type `yes` and continue.

You may also see the following if you failed to run the `chmod 400` command in the above screenshot:

```
	WARNING: UNPROTECTED PRIVATE KEY FILE!
```

If you do, just run that command and try again.

![first-connection](images/ec2-13-first-connection.png)

### AWS Credentials

Now, we will try to use the AWS CLI which is installed by default on Amazon Linux 2.

You can run `aws --version` to check the installed version of the CLI, and then try `aws s3 ls` to list your s3 buckets.

![aws-cli-no-creds](images/ec2-14-aws-cli-no-creds.png)

The AWS CLI will tell you that it is not configured and that you can configure it with `aws configure`. However, we are going to do something different. Because EC2 instances run in AWS on your account, they can be directly configured with access to the services you wish.

To do this, visit the [EC2 Console](https://us-east-2.console.aws.amazon.com/ec2/home?region=us-east-2#Instances:instanceState=running) again and select your running instance, and then click "**Actions** > **Security** > **Modify IAM role**".

![actions-security](images/ec2-15-actions-security.png)

Now, we will create a new IAM role to attach to our instance.

![modify-iam-create](images/ec2-16-modify-iam-create.png)

The IAM Dashboard should open in a new tab where we will click "**Create role**"

![iam-dashboard](images/ec2-17-iam-dashboard.png)

We will select **AWS service** and **EC2** as our trusted entity (this means that the EC2 service is the identity allowed to "assume" this role and gain its defined permissions). Click Next once you've done this.

![iam-create-role](images/ec2-18-iam-create-role.png)

![iam-add-permissions](images/ec2-19-iam-add-permissions.png)

Give your Role a useful name and description, then scroll down to review.

![iam-name-role](images/ec2-20-iam-name-role.png)

Confirm the policies and click **Create role**.

![iam-review](images/ec2-21-iam-review.png)

Once created, you'll see the following confirmation page. You may now close this tab to return to the EC2 Modify Role page.

![iam-complete](images/ec2-22-iam-complete.png)

You may need to refresh the role list, and then choose your new role from the dropdown. Once selected, you can click **Update IAM role**.

![modify-iam-add-role](images/ec2-23-modify-iam-add-role.png)

You should see the following confirmation page.

![role-added](images/ec2-24-role-added.png)

Back in your terminal connect to the EC2 instance if you are no longer connected, and run the following commands

```shell
aws sts get-caller-identity
aws s3 ls
```

This will show you that you are authenticated as an "assumed-role" using the role we just created and attached to the instance. You should be able to perform s3 actions, but nothing else.

![aws-cli-creds](images/ec2-25-aws-cli-creds.png)

### Cleanup

Lastly, you should terminate this instance once you are done with it. From the EC2 Instances Dashboard, select the instance and then click "**Instance state** > **Terminate instance**".

> Note, this is a destructive action and will delete the instance and it's state from your account. Instances can be configured to keep their EBS volume around after the instance itself is deleted which will allow for recovery in the case of accidental termination.

![terminate](images/ec2-26-terminate.png)
