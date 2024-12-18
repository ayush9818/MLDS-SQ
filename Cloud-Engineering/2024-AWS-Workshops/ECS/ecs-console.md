# AWS ECS Tutorial

See [the README](./README.md) for more information on the ECS Service.

For this course, we will be deploying our resources manually using the AWS ECS Console.

## Summary of Steps

0. ECR Tutorial
1. Task Definition
2. Cluster
3. Service
4. Check Security Groups
5. Test Connection

- [AWS ECS Tutorial](#aws-ecs-tutorial)
  - [Summary of Steps](#summary-of-steps)
  - [Tutorial](#tutorial)
    - [ECR](#ecr)
    - [Cluster](#cluster)
    - [Iris Pipeline Task Definition](#iris-pipeline-task-definition)
    - [Iris Pipeline Task](#iris-pipeline-task)
    - [Iris Inference Task Definition](#iris-inference-task-definition)
    - [Iris Inference Service](#iris-inference-service)
    - [Modify ECS Security Group](#modify-ecs-security-group)
    - [Service is Live!](#service-is-live)
    - [Modify RDS Security Group](#modify-rds-security-group)
    - [Pushing New Images](#pushing-new-images)
      - [Restarting Service](#restarting-service)
      - [Updating Task Definitions](#updating-task-definitions)
    - [Scaling Down](#scaling-down)
  - [Note on Load Balancers](#note-on-load-balancers)

## Tutorial

As always, navigate to the AWS Console and ensure you are in the right region.

Start at the [ECS Console](https://us-east-1.console.aws.amazon.com/ecs/v2/home?region=us-east-1)

![ECS Console - v2 Home](./images/ecs-console/ecs-console-v2.png)

### ECR

Be sure to complete the [ECR Tutorial](./ecr-repo.md) before continuing on.

---

### Cluster

![Clusters - Create](./images/ecs-console/ecs-cluster-00.png)

From the clusters home page, click on **Create cluster** to get started.

---

![Cluster Create - Config](./images/ecs-console/ecs-cluster-01.png)

Give your cluster a name like `mlds-ecs-workshop`

---

![Cluster Infrastructure](./images/ecs-console/ecs-cluster-02.png)

- Check the Amazon EC2 Instances box, and configure the compute provider appropriately for free-tier
- Select "On-demand", and confirm that "Amazon Linux 2" is being used
- Ensure that `t2.micro` is being used
- Set the maximum capacity to 1 so that it does not scale past free tier
- Choose the ssh key pair you created in the EC2 tutorial

> Fargate is not free-tier-eligible so we will first create the cluster to use a free-tier-eligible EC2 instance; however, we will leave Fargate enabled as well for demonstration purposes.

---

![](ecs-cluster-02b.png)

- Configure your networking so that the created autoscaling group uses only the default subnets in your default VPC
- Create a new security group
- Allow inbound SSH from the Northwestern VPN range (`165.124.160.0/21`)

---

![Cluster Details - Deploy](./images/ecs-console/ecs-cluster-03.png)

You should see a confirmation page after a few minutes once the cluster is created. From here, click on the Task Definitions link on the left sidebar.

---

<details>
  <summary>If you see an error after clicking "Create Cluster"</summary>

Sometimes, an error like this can randomly happen

![Alt text](./images/ecs-console/ecs-cluster-error-01.png)

Just click on the "View in CloudFormation" button

![Alt text](./images/ecs-console/ecs-cluster-error-02.png)

Then click "Retry"

![Alt text](./images/ecs-console/ecs-cluster-error-03.png)

Confirm "Retry"

![Alt text](./images/ecs-console/ecs-cluster-error-04.png)

And wait for it to finish completing

</details>

---

### Iris Pipeline Task Definition

![ECS Home - Task Definitions](./images/ecs-console/ecs-home-taskdef.png)

First, we will create a Task Definition that informs ECS how our application should be run. From the ECS Console Home page, click on the [Task definitions](https://us-east-1.console.aws.amazon.com/ecs/v2/task-definitions?region=us-east-1) link in the sidebar.

---

![Task Definitions - Create](./images/ecs-console/ecs-task-definition-00.png)

You should now see an empty listing of Task definitions... you should click the **Create new task definition** button to start creating a new Task definition.

---

![Task Definitions - Configure Containers](./images/ecs-console/ecs-task-definition-01.png)

1. You may change the name of your Task definition if you like, or use `iris-pipeline` for consistency.
2. You **MUST** change the networking mode away from the default `awsvpc` to **`bridge`**. 
3. You do not have to specify CPU requirements for EC2 launch type, but you can set it to `0.25 vCPU` to be explicit
4. Set the memory to `0.5 GB`
5. You may name the container anything you like, but you **must** provide the proper Image URI that you copied during the [ECR Tutorial](./ecr-repo.md#copy-ecr-image-uri)
6. Remove the container port setting as this application does not expose any ports
7. Set any environment variables that your application relies on (such as `BUCKET_NAME`)

![Alt text](./images/ecs-console/ecs-task-definition-02.png)

Click **Next** to move on to the next configuration step.

---

**IFF** you are trying the Fargate launch type, you will have to use `awsvpc` network mode, and must select your task size from the dropdowns.

![Task Definitions - Configure Env](./images/ecs-console/task-def-configure-env.png)

1. Ensure that the architecture is set to Linux/x86_64*
2. Change the CPU and Memory settings to their minimum (`.25 vCPU`, `.5 GB`)

> NOTE: it may display a warning about incompatible selection after you set the memory to `.5 GB`; just click on the CPU setting again and set it to `.25 vCPU` again.

> NOTE: you _may_ need to set these configurations to a higher value if your application is particularly compute/memory intensive and crashes with the minimum alloted cpu/mem. Increasing these values will increase the $/minute that your ECS Service charges and will likely consume all of your ECS free credits if you do not closely monitor/control it. If this is relevant to you, please reach out to the instructors about your situation.

> *Linux/x86_64 has been the dominant architecture for a long time and ECS has traditionally required images to be built for this platform. With the rising popularity of ARM architectures (largely due to Apple's M1 chip), ECS has started to support different architecture runtimes in ECS. We will continue using x86_64 for this course and will build compatible images via the `--platform` option if your host machine uses an ARM or other architecture.

---

![Logging settings](./images/ecs-console/ecs-task-definition-04.png)

You can leave all other settings as default and click **Next** to continue.

On the **Review and create** page, confirm your settings and click **Create** to continue.

---

![Created](./images/ecs-console/ecs-task-definition-05.png)

After a few seconds, you should be taken to a page which shows the details of your task definition.

---

### Iris Pipeline Task

We will now use the Task Definition to run a "Task" or job with the iris-pipeline configuration.

---

![Alt text](./images/ecs-console/ecs-task-00.png)

From the task definition, click on "**Deploy**" and "**Run task**".

---

![Alt text](./images/ecs-console/ecs-task-01.png)

Select your cluster from the drop-down and choose Capacity provider (or Launch Type: Fargate if you are using Fargate).

You may accept all other defaults and click "**Create**"

---

![Alt text](./images/ecs-console/ecs-task-03.png)

You can now watch the task as it goes through the provisioning and running process. It may take some time to provision and run, especially if you choose EC2 and have to wait for a new instance to be deployed.

Eventually, the task will show "Running" and you can click into the task to view its details.

---

![Alt text](images/ecs-console/ecs-task-04-logs.png)

Click into the "**Logs**" tab to see the logs from the run...

Our application was unable to connect to S3 because it does not have any aws credentials to use. Similarly to how we attached an IAM role to the EC2 intsance we created in the [EC2 Tutorial](../EC2/Activity.md), we can attach an IAM Role to the ECS Task.

---

NOTE: if your task ran and stopped and you are having trouble finding it, you may have to show "Stopped Tasks" from the Tasks view of the Cluster dashboard

![Alt text](images/ecs-console/ecs-task-05-view-stopped.png)

![Alt text](images/ecs-console/ecs-task-06-stopped-tasks.png)

---

Now, let's add a TaskRole to the TaskDefinition for Iris Pipeline

![Alt text](images/ecs-console/ecs-task-07-task-defs.png)

Navigate back to the Task Definitions view and click on your task definition for iris-pipeline

---

![Alt text](images/ecs-console/ecs-task-08-td-create-rev.png)

Select the active (latest) task definition revision and then click on "Create new revision". (Task definitions cannot be modified in place, but instead you create new revisions so that if you break something, it is easy to "rollback" to an old revision).

---

![Alt text](images/ecs-console/ecs-task-09-modify-td.png)

Scroll down to the "**Infrastructure**" section and click the IAM Console link to go create a new IAM Role for ECS Tasks.

---

![Alt text](images/ecs-console/ecs-task-10-iam-create-role.png)

From the IAM Dashboard, click "**Create role**"

---

![Alt text](images/ecs-console/ecs-task-11-iam-trust-policy.png)

Configure your trust policy for ECS by typing "*Elastic Container Service*" into the search box for "**Service or use case**".

Then, select "**Elastic Container Service Task**"

---

![Alt text](images/ecs-console/ecs-task-12-iam-add-policy.png)

Add the `AmazonS3FullAccess` Policy as we did previously for our EC2 Role.

---

![Alt text](images/ecs-console/ecs-task-13-iam-review.png)

Give the Role a name (like `ecs-iris-tasks`), review the details, and create it.

Once the role is created, you may close this tab and return to the Task Definition page we were on previously.

---

![Alt text](images/ecs-console/ecs-task-14-td-select-role.png)

You should now be able to select the newly created role from the drop-down and assign it to the Task Definition.

---

![Alt text](images/ecs-console/ecs-task-15-deploy-task.png)

Now that the new revision has been created, we will launch another task which will make use of the IAM role specified in the new task definition.

---

![Alt text](images/ecs-console/ecs-task-16-task-created.png)

Again, the task may take a few minutes to provision, but then we can click into it and view its configuration and logs.

![Alt text](images/ecs-console/ecs-task-17-pipeline-task.png)

### Iris Inference Task Definition

Now, we will repeat the same process but for the Iris Inference web application.

![Alt Text](images/ecs-console/ecs-service-01-new-td.png)

Navigate back to the Task definitions page and click "**Create new task definition**".

---

![Alt Text](images/ecs-console/ecs-service-02-inference-td.png)

1. Give the task definition a name (like `iris-inference`)
2. Set the network mode to `bridge`
3. Set the memory limit (and optionally set the cpu limit)
4. Specify the `ecs-iris-tasks` role we just created

---

![Alt Text](images/ecs-console/ecs-service-03-inference-env.png)

1. Give the container a name (like `inference`)
2. Copy and past the image URI from the ECR repository you created for `iris-inference` images (note, it will be different than what's shown in my screenshot).
3. Explicitly set the **Host port** to `80` and ensure the container port is also set to `80` (since that's the port on which we run our container as set in our `Dockerfile`)
4. Add an environment variable for `BUCKET_NAME` with a value of the bucket in  your account you will use with this application. NOTE: this will be a different value than the bucket name shown in my screenshot.
5. Click "Next" when you are done.

---

### Iris Inference Service

![Alt Text](images/ecs-console/ecs-service-04-inference-service.png)

From the task definition page for iris-inference, click "Deploy" and "Create service".

---

![Alt Text](images/ecs-console/ecs-service-05-create.png)

1. Select your cluster from the drop-down.
2. Specify the launch type or provider strategy

---

![Alt Text](images/ecs-console/ecs-service-06-config.png)

Give your service a meaningful name (like `iris-app`)

---

**IFF** you are using Launch Type: Fargate, you will likely want to configure a Load Balancer! If you are using Launch Type: EC2, this is not necessary.

<details>
  <summary>Load Balancer Information...</summary>


![Alt Text](images/ecs-console/ecs-service-07-alb.png)

Configure an Application Load Balancer to direct traffic to your application.

1. Change Load balancer type to be "Application Load Balancer"
2. Select "Create a new load balancer"
3. Give your load balancer a meaningful name like `iris-inference`
4. Confirm the Listener port to be `80` and Protocol: `HTTP`
   1. This is the port and protocol where users will "find" your application
5. Give your target group a meaningful name like `iris-inference` and ensure Protocol: `HTTP`
6. Set the Health check path to `/`
7. Set the Health check grace period to `10`

> We use an Application Load Balancer (ALB) here so that users can consistently find and communicate with our application. ECS Containers may be decommissioned and redeployed often and will have a new IP address each time. The ALB keeps track of this via a "Target Group" which will register the IP address of new containers as they come online. With the ALB deployed, we can just direct users to the static DNS name of our ALB and let it handle the routing of requests to the appropriate container based on the configured Listeners and Target Groups. Read more about ALB's [below](#note-on-load-balancers)
</details>

All other settings can be left default, click **Deploy** to continue.

---
<!-- 
![Deployment - Networking](./images/ecs-console/deployment-config-networking.png)

1. Ensure that the VPC is set to the default VPC in your account
2. Select "Create a new security group"
3. Give your security group a meaningful name and description like `mlds423-ecs-access`, `Allow access to mlds423 ECS Service`
4. Click "Add new rule" and set the **Type** to `HTTP`, **Source** to `Custom`, and **Values** to `165.124.160.0/21` ([Northwestern VPN CIDR Block](https://nuinfo-proto2.northwestern.edu/network/secure/configuration.html))

---
-->

![Alt Text](images/ecs-console/ecs-service-08-created.png)

After a few minutes, if all the steps were completed successfully, you will get a confirmation that the service has successfully deployed.

---

![Alt Text](images/ecs-console/ecs-service-09-service-health.png)

From the deployed service page, you can view some important details about your deployed service such as health, logs, and networking

![Alt Text](images/ecs-console/ecs-service-10-logs.png)

The logs displayed here can help you troubleshoot your application as it is deployed in ECS.

---

Only if you are using Fargate and an Application Load Balancer...

![Alt Text](images/ecs-console/ecs-service-11-networking.png)

The networking tab has helpful information about your service

1. First, we will need to modify the security group to allow web traffic (port 80) from the NU VPN to the configured security group
2. Then, copy or open the DNS name for your application load balancer; this is where you can access your application on the internet! (you will not be able to access this page until you've modified the security group)

> NOTE: Technically, we need to allow HTTP traffic from NU VPN to our _Load Balancer's_ security group, and _then_ allow traffic from the Load Balancer to the Container. Typically you would have a different security group attached to each of these resources (one for Task, one for ALB). However, when we created our service, we left the default networking configuration in place which will attach our VPC's "default" security group. (SG) The same SG is used for the ALB (and cannot be changed when creating an ALB through the ECS Console at the time this workshop is being written). Because of this, we can add a single rule allowing web traffic from NU VPN into the default SG. The default SG already has a rule configured to allow traffic on all ports *within* the SG (meaning resources belonging to the same SG can talk to each other freely).

```text
dynamic IP               AWS-assigned DNS
+------+     +--------+      +-----+      +----------+
|      |     |        | port |     | port |          |
|  PC  | --> | NU VPN | ---> | ALB | ---> | ECS Task |
|      |     |        |  80  |     |  80  |          |
+------+     +--------+      +-----+      +----------+
          165.124.160.0/21               some dynamic IP
```

---

### Modify ECS Security Group

![Alt Text](images/ecs-console/ecs-service-12-sg.png)

From the Security group page, click on Edit inbound rules

![Alt Text](images/ecs-console/ecs-service-13-sg-rule.png)

1. Add a new rule
2. Set its type to be `HTTP`
3. Set the Custom Source to the NU VPN CIDR: `165.124.160.0/21`
4. Add a description
5. Save Rules

### Service is Live!

Back in your browser tab you can navigate to the Public IP Address of the EC2 Instance (or if you are using Fargate/ALB: the DNS name for the load balancer obtained from the service's Networking tab) and go to the "/docs" url to view the FastAPI auto-generated docs for our web app.

![Alt Text](images/ecs-console/ecs-service-14-docs.png)

---

### Modify RDS Security Group

If you need to connect to an RDS Database from your deployed ECS Service, you'll need to create a new Inbound Rule on your RDS Security Group to allow this connection. This can be done from the Console by following the steps below:

First you'll need to identify the security group used for your ECS Service.

1. Navigate to the ECS Console
2. Click on your created cluster
3. Click on the running service
4. Click on the security group listed under "Networking"

---



1. Copy the security group ID by clicking on the "copy" icon next to the ID
2. Go back to the security group listing by clicking on "Security Groups" in the breadcrumb

---



Now we can add a rule to our RDS security group; click on the rds-access security group from the list.

---

![Security Group - RDS Access](./images/ecs-console/sg-rds-access.png)

Click on **Edit inbound rules** for the mlds423-rds-access security group.

---

![Security Group - RDS Inbound Rules](./images/ecs-console/sg-rds-inbound-rules.png)

1. Set Type to MySQL/Aurora
2. Set the source to "Custom" and then in the search bar select the security group that is used for your ECS service.
3. Give the rule a meaningful description like "Inbound access from ECS"
4. Save rules

After a few seconds, you should see a modification confirmed page.

![Security Group - Modified](./images/ecs-console/sg-rds-modified.png)

---

### Pushing New Images

You can build and push new images to the ECR repo as needed.

If you push a new image to ECR, using the same tag already in use (like `latest`), you'll just restart the service as noted [below](#restarting-service). If you need to update your Task Definition to use a different tag, you'll follow the steps in [Updating Task Definition](#updating-task-definitions)

#### Restarting Service

If you need to "restart" your service, you can simply stop the running tasks. This will cause ECS to launch a new task to replace it (and keep your running task count at `1` as configured by your service). When ECS launches the new task, it will pull the new image.

![Stop Task](./images/ecs-console/ecs-stop-task.png)

A more proper way to do this would be to select the service, click "Update service", and then select "Force new deployment", changing nothing else.

#### Updating Task Definitions

If you need to update or change your Task Definition later (add environment variables, update the image tag being used, etc.), you can do so simply from the [Task Definition Console](https://us-east-1.console.aws.amazon.com/ecs/v2/task-definitions?region=us-east-1).

![Create New Revision](./images/ecs-console/td-create-revision.png)

1. Choose the latest revision (base for new updates)
2. Click "Create new revision"

Then, simply update the fields required, and save the changes. This will result in a new revision being added to the Task Definition Family.

---

Now, we need to update our ECS Service to use the new revision.

![Edit Service](./images/ecs-console/ecs-edit-service.png)

1. View services in your cluster
2. Select the service for editing
3. Click "Edit service

---

![Update the Task Definition](./images/ecs-console/ecs-edit-service-td.png)

1. Update the Task Definition to the latest "Revision"
2. Click "Update" to confirm

---

### Scaling Down

If you want to momentarily stop your service (prevent charges from accruing, etc.), you can scale it down to 0 tasks.

Select the service for editing as done in the "Edit Service" step above.

![Scale Down](./images/ecs-console/ecs-edit-service-scale.png)

1. Set the "Desired tasks" to 0
2. Click "Update" to confirm

You can follow the same steps to scale back up, just change "Desired tasks" to 1.

---

## Note on Load Balancers

An Application Load Balancer (ALB) will have a fixed address that we can visit in the browser. It will then route our requests to the containers serving our application. This is done with the help of a "Listener" and a "Target Group". We will point our load balancer to the target group, and then register our containers as "targets" in that group. Listeners receive requests on a specific port and based on "Rules" will determine how a request is routed to an appropriate target group. Rules can select the right target group based on things like URL path, request headers, and more.

ALB's can also help spread out our requests to multiple instances of our application, even if their own addresses are changing. This is helpful if you have a lot of traffic all at once and need to evenly distribute the load across several "workers".
	