#!/bin/bash

if [[ -n $(git status --porcelain) ]]; then
    echo "Error: There are uncommitted changes in the repository."
   # exit 1
fi

#git pull origin main

set -x
set -e

export COMMIT_HASH=$(git rev-parse --short HEAD)
export AWS_REGION=us-east-2
export IMAGE_NAME=labelforce
export IMAGE_TAG=$(date +"%Y-%m-%d").1.$COMMIT_HASH
export ECR_REGISTRY=226332508888.dkr.ecr.us-east-2.amazonaws.com

# Login to ECR
aws ecr get-login-password --region us-east-2 | \
    docker login --username AWS --password-stdin ${ECR_REGISTRY}

# Build image by running this command in Dockerfile directory 
docker build -t ${IMAGE_NAME} --no-cache --provenance=false .

docker tag ${IMAGE_NAME} \
    ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

# Push image to ECR
docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
