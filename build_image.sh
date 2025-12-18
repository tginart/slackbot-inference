#!/usr/bin/env bash

# If invoked with `sh build_image.sh`, re-exec under bash (dash doesn't support pipefail / [[ ]]).
if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi

set -euo pipefail
set -x

if [[ -n $(git status --porcelain) ]]; then
  echo "Error: There are uncommitted changes in the repository."
 # exit 1
fi

export AWS_REGION=us-east-2
export IMAGE_NAME=labelforce
export COMMIT_HASH=$(git rev-parse --short HEAD)
export IMAGE_TAG=$(date +"%Y-%m-%d").1.$COMMIT_HASH
export ECR_REGISTRY=226332508888.dkr.ecr.us-east-2.amazonaws.com
export IMAGE_URI=${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

# Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | \
  docker login --username AWS --password-stdin ${ECR_REGISTRY}

# ---------------------------------------------------------------------------
# Build + push (buildx)
# ---------------------------------------------------------------------------
# Ensure buildx is available (Docker Desktop typically has it).
docker buildx version >/dev/null

# Build + Push (SageMaker needs a Linux image; on Mac we must build linux/amd64)
docker buildx build \
  --platform linux/amd64 \
  -t ${IMAGE_URI} \
  --no-cache \
  --provenance=false \
  --push \
  .

echo "Pushed image: ${IMAGE_URI}"
