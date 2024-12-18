# Elastic Cloud Compute (EC2)

Here we will introduce the fundamentals of the EC2 Service. See [Activity.md](./Activity.md) for a walkthrough on configuring, deploying, and connecting to a basic EC2 Instance.

## Introduction

Amazon Elastic Compute Cloud (EC2) is a web service offered by Amazon Web Services (AWS) that allows users to launch and manage virtual machines (Instances) in the cloud. Essentially, EC2 provides resizable compute capacity in the cloud, allowing users to quickly and easily provision virtual machines to meet their computing needs. It is the most basic and foundational service that AWS offers.

EC2 is important because it provides a number of benefits that make it an attractive solution for businesses and organizations of all sizes. These benefits include:

1. Scalability: EC2 instances can be easily scaled up or down based on changing computing needs. This allows businesses to quickly respond to changes in demand, without the need for costly infrastructure investments.

2. Flexibility: EC2 instances can be launched in a variety of configurations, including different instance types, operating systems, and software configurations. This allows businesses to tailor their computing environments to their specific needs.

3. Cost savings: EC2 instances are billed on a pay-as-you-go model, allowing businesses to only pay for the computing resources they actually use. This can result in significant cost savings compared to traditional on-premises computing solutions.

4. High availability: EC2 instances can be launched in multiple availability zones, ensuring high availability and redundancy in the event of hardware or network failures.

5. Security: EC2 provides a number of security features, including virtual private cloud (VPC) support, security groups, and the ability to encrypt data at rest and in transit. This allows businesses to ensure their computing environments are secure and compliant with industry regulations.

Overall, EC2 is an important tool for businesses and organizations looking to quickly and easily provision computing resources in the cloud. Its flexibility, scalability, and cost-effectiveness make it a popular choice for a wide range of use cases, from small startups to large enterprises. Essentially, every other service that AWS offers is just a high-level managed service that people commonly ran on EC2.

### Instance Types

Servers in EC2 are categorized as Instance Types. Each Type has a specific amount of CPU and Memory available as well as various other properties. Each Instance Type also has a corresponding price that reflects these properties (e.g. more compute = higher price).

Instance Types use a name that encodes their properties: `t3.nano` = `t` family (burstable), `3`rd generation, `nano` size with `0.5 GiB` memory and `2 vCPU` for a 1h 12m burst. Some instance types have much longer names to indicate their additional features. For example: `g4dn.xlarge` has an NVIDA Tesla T4 GPU and `16 GiB` memory with `4 vCPU`

These Types can be grouped into "Families" that reflect their general design. For example, the "Compute Optimized" Family (e.g. `c5`) uses `c`, the "General Purpose" Family (e.g. `m5`) uses `m`, and the "Burstable Family" (e.g. `t3`) uses `t`.

Burstable instances do not have the full amount of allocated vCPU available to them 24/7, but instead "stock up" CPU credits while idling, and then expend these credits in "bursts" of high-compute. This makes them good at tasks such as web servers with unpredictable traffic, data processing pipelines with sporadic throughput, etc. They are generally quite a bit cheaper as well which makes them good candidates for development and testing.

A great website for identifying a suitable instance type for your need is [Instance Info by Vantage](https://instances.vantage.sh/). I use this website all the time and it has been around for a long while.

You can also browse this information on the official [AWS Instance Types](https://aws.amazon.com/ec2/instance-types/) page

## AMIs

An Amazon Machine Image (AMI) is a pre-configured virtual machine image that contains all the information necessary to launch an instance in the cloud. An AMI includes the operating system, any installed applications, and any necessary configuration settings. Users can choose from a variety of publicly available AMIs or create their own custom AMIs to meet their specific needs. AMIs provide a fast and easy way to launch instances in the cloud without the need for manual configuration. They also allow users to launch multiple instances with the same configuration, making it easy to scale up or down as needed.

You can create an AMI from an existing instance that has been configured for a specific job; e.g. install machine learning dependencies, configure your bash profile, and set up a folder structure for data science projects.

## EBS Volumes

Amazon Elastic Block Store (EBS) is a storage service that provides highly available and scalable block-level storage volumes for use with Amazon EC2 instances. EBS volumes are designed for mission-critical workloads that require high levels of durability and availability. Users can choose from a variety of EBS volume types, including General Purpose SSD, Provisioned IOPS SSD, and Throughput Optimized HDD, to meet their specific performance and cost requirements. EBS volumes can be attached to EC2 instances and can be used as the primary storage for applications, databases, and file systems. They are also highly flexible, allowing users to easily create, modify, and delete volumes as needed.

Typically you will just use a General Purpose SSD that is connected to your EC2 instance when you deploy the instance. You may however want to migrate everything from one instance to another. You can easily do this by stopping the instance, detaching the EBS volume, and then mounting it to a new EC2 instance.

## Networking

Cloud networking is a very deep and complicated topic. I will share some material that covers this more in-depth at a later time; for now we will introduce just the basics.

### VPC

Many AWS services are deployed into public network space owned by AWS (S3, SQS, etc.). These services are accessible over the public internet and access must be managed with IAM controls. Others (EC2, RDS, etc.) are deployed into a private network space owned and managed by an account; this is referred to as a "Virtual Private Cloud (VPC)". This is a network that AWS deploys for you, but you then have complete control over (and responsibility for) its configuration. Other services still (Lambda, etc.) can be deployed in the public AWS network *or* into VPC that you manage.

### Subnets

Each VPC can be divided up into several "Sub Networks (subnets)". Each of these subnets can be configured and managed differently to enable various networking designs. The default VPC will have several **Public** subnets and several **Private** subnets.

Resources in public subnets can be reached from the internet. Resources in private subnets can only be reached by other resources in the same VPC.

### Security Groups

Security Groups are how you control connections to and from various resources in a VPC. Every resource in a VPC will have an associated security group. By default, the security group will not allow any *inbound* connections but will allow all *outbound* connections. This means you will not be able to connect to the server unless you add rules to the security group.

## Connecting to Your Instance

There are a few different ways to connect to an EC2 instance these days. We will introduce a couple of them:

1. SSH: The most common method for connecting to a Linux-based EC2 instance is to use SSH (Secure Shell) to establish a secure shell connection to the instance. To use SSH, you will need to have the private key file associated with the instance's public key.

    Note: you will have to create a key-pair in the AWS console, download the private key file, associate the instance with the created key-pair, and then connect using the private key you downloaded.

2. RDP: If you are using a Windows-based EC2 instance, you can connect to it using Remote Desktop Protocol (RDP). To use RDP, you will need to have the administrator password for the instance.

3. AWS Systems Manager Session Manager: AWS Systems Manager Session Manager allows you to manage your EC2 instances remotely using a web-based console. You can start a session with an instance from the console, and then use the session to run commands or troubleshoot issues. Note: this requires the SSM-agent to be installed on the instance and for IAM permissions to be configured correctly. See [AWS SSM Docs](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started.html) for more info.

4. AWS EC2 Instance Connect: This is available for some instances and makes it very simple to connect to your instance via the AWS Console. See [AWS Docs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-set-up.html) for more info.

The method you choose for connecting to your EC2 instance will depend on your specific needs and the tools you are comfortable using. It's important to ensure that your connection to the instance is secure and that you have the necessary credentials to access the instance.

## Pricing

### On-Demand vs Spot

Most of the time you will deploy what's called an "on-demand" instance. This gives you full control over the instance and is the most flexible. However, for a significant cost savings, you can deploy a "spot" instance. These can be up to 70% cheaper than on-demand, but are allocated on a supply-and-demand basis. You essentially place a bid on some instance type and so long as their are instances available, you will pay that reduced price. However, as soon as surplus instance supply is used up, your instances will be re-allocated to the next highest bidder. This model is well-suited to workloads that can be interrupted frequently and typically requires some careful design.

### Instance Reservations and Savings Plans

The other way to save money on EC2 is to commit to a set amount of spending up-front. Previously, this was usually done by "reserving" an instance for 1 or 3 years similarly to how you may purchase a traditional server for a project. If you outgrew or did not fully utilize that reserved instance, there was no way to re-size it once reserved. However, AWS has introduced Savings Plans in recent years which allows you to commit to some dollar-amount spend over 1 or 3 years. This spend commitment still gets you a highly discounted rate, but can be applied to any of the EC2 instances you deploy as well as some serverless compute such as ECS Fargate containers.

## EC2 Metrics

Amazon EC2 provides various metrics that you can use to monitor your instances and detect any issues. These metrics fall into three categories: default available metrics, enhanced metrics, and custom metrics.

1. Default Available Metrics: Amazon CloudWatch provides default metrics for EC2 instances, such as CPU utilization, disk read/write, and network traffic. These metrics are available for free and are automatically collected at a five-minute interval. You can view these metrics in the CloudWatch console and use them to monitor the performance of your instances and troubleshoot any issues.

2. Enhanced Metrics: Enhanced monitoring provides additional metrics for EC2 instances, such as per-process metrics, disk I/O operations, and network packets. Enhanced metrics are collected at a one-minute interval. Enhanced monitoring is available at an additional cost.

3. Custom Metrics: Custom metrics allow you to monitor application-specific metrics that are not included in the default or enhanced metrics. You can publish custom metrics to CloudWatch using the CloudWatch API or SDK, and then use CloudWatch to visualize and alert on these metrics. Custom metrics are also available at an additional cost.

By using EC2 metrics, you can gain visibility into the health and performance of your instances, and identify any potential issues before they impact your applications. It's important to select the appropriate metric based on your needs and monitor them regularly to ensure that your EC2 instances are performing optimally.

## Autoscaling Groups

Auto Scaling Groups (ASGs) are a feature of Amazon EC2 that allow you to automatically scale the number of EC2 instances in your application based on demand. ASGs help you maintain the desired level of application availability and performance while minimizing costs.

ASGs work by defining a group of EC2 instances that share similar characteristics and are managed as a single entity. You can configure the ASG to automatically launch or terminate instances in response to changes in demand, such as increased traffic to your application.

The use case for ASGs is to ensure that your application is always available and performing optimally, even during periods of high demand. With ASGs, you can quickly scale your application up or down as needed, without the need for manual intervention. This helps you save costs by only running the required number of instances, while still maintaining the desired level of performance.

ASGs are commonly used in scenarios such as web applications, e-commerce sites, and other applications that experience fluctuating traffic. By using ASGs, you can ensure that your application can handle increased traffic without affecting its performance, while also avoiding over-provisioning of resources during periods of low demand.

## Conclusion

Amazon EC2 is a powerful and flexible cloud computing service that provides you with the ability to launch and manage virtual servers in the cloud. This probably felt like a lot of content, but EC2 is the most foundational service in AWS and deeply configurable to your needs. You may not have to know the above concepts very deeply, but it is good to at least be aware of them so you can reference or research when necessary.

By understanding these concepts and best practices, you can leverage EC2 to deploy scalable, resilient, and cost-effective applications on the cloud. Whether you're building a simple web application or a complex data pipeline, EC2 provides you with the tools you need to build and scale your infrastructure as needed. With this knowledge, you can confidently deploy and manage EC2 instances in the cloud, and take full advantage of the benefits that cloud computing has to offer.

We will now deploy a simple EC2 Instance to demonstrate some of the above.

[Activity.md](./Activity.md)
