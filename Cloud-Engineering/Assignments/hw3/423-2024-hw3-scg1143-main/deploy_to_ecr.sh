#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <aws_account_number> <local_image_name> <ecr_tag>"
  exit 1
fi

# User Parameters
AWS_ACCOUNT_NUMBER=$1
LOCAL_IMAGE_NAME=$2
ECR_TAG=$3
AWS_REGION="us-east-1"
ECR_REPOSITORY_URI="${AWS_ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com/cloud-app:${ECR_TAG}"

# Step 1: Retrieve an authentication token and authenticate your Docker client to your registry
echo "Authenticating Docker client to AWS ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${AWS_ACCOUNT_NUMBER}.dkr.ecr.${AWS_REGION}.amazonaws.com


# Step 2: Tag the Docker image
echo "Tagging Docker image with ECR URI ${ECR_REPOSITORY_URI}..."
docker tag ${LOCAL_IMAGE_NAME} ${ECR_REPOSITORY_URI}

# Step 3: Push the Docker image to the AWS ECR repository
echo "Pushing Docker image to ECR repository ${ECR_REPOSITORY_URI}..."
docker push ${ECR_REPOSITORY_URI}

echo "Docker image ${LOCAL_IMAGE_NAME} successfully pushed to ${ECR_REPOSITORY_URI}"
