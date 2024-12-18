# AWS ECS Getting Started

This tutorial will walk through the Getting Started Wizard provided by AWS ECS.

## Tutorial

### Summary of Steps

0. ECR Tutorial
1. Getting Started Wizard
2. Security Groups

### ECR

Be sure to complete the [ECR Tutorial](./ecr-repo.md) before continuing on.

### Create ECS Deployment

We will make use of the ECS Getting Started wizard to simplify deployment; however, each of these steps can be performed individually from the console in the order of: `cluster -> task definition -> service`

#### ECS Wizard

![ECS Get Started Wizard](images/ecs-getting-started/ecs-0-get_started.png)

Navigate back to the [ECS Dashboard](https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/getStarted) as done in [step 0](#tutorial). This time, click on the "Get Started" button (link).
<!-- TODO: Add link to Get Started Wizard -->

#### ECS Custom Container

![ECS Get Started Wizard](images/ecs-getting-started/ecs-1-custom_template.png)

Click on "custom" for the Container definition, and then click "Configure" to define your custom container.

![ECS Get Started Wizard](images/ecs-getting-started/ecs-2-custom_container.png)

Name your container whatever you like, but input the "Image" uri as obtained from your ECR Repo in [step x](#copy-ecr-image-uri). **Be sure to append the image tag that you used when you pushed; this is likely "latest"**; your full Image URI should look like `1234567890.dkr.ecr.us-east-1.amazonaws.com/mlds423-flask:latest`

![ECS Task Definition Environment](images/ecs-getting-started/ecs-3-container_env.png)

Under "Advanced", scroll down to "Environment", and add any environment variables that your application needs.

#### ECS Task Definition

![ECS Edit Task Definition](images/ecs-getting-started/ecs-4-edit_task_def.png)

![ECS Task Definition Details](images/ecs-getting-started/ecs-5-task_def_custom.png)

Edit your task definition and set the following basic details.

![ECS Create Task Definition](images/ecs-getting-started/ecs-6-create_confirm.png)

Confirm your details and create task definition.

#### ECS Service

![ECS Define Service](images/ecs-getting-started/ecs-7-service.png)

Select "Application Load Balancer" and then edit your service details.

![ECS Service Details](images/ecs-getting-started/ecs-8-service_details.png)

Edit your service's details and set the security group cidr block to `165.124.160.0/21`.

### ECS Cluster

![ECS Cluster](images/ecs-getting-started/ecs-9-cluster.png)

Name your cluster and click next to continue.

### Confirm and Create

![ECS Confirmation](images/ecs-getting-started/ecs-10-confirm.png)

Validate the settings and confirm creation. This may take a few minutes.

![ECS Created](images/ecs-getting-started/ecs-11-creation_complete.png)

### Security Groups

Edit the Ingress Rules for your RDS Security Group (`DB-SG`) to allow MySQL traffic (port 3306) from the Application Security Group (`App-SG`).

<!-- TODO: Explicit Steps -->
