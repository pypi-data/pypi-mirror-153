#!/bin/bash
## @file
## This script is part of the cloud evaluation scripts, it runs on the aws service from the downloaded source tag,
## its main purpose is to execute 'docker build' to build an image using the Dockerfile that was downloaded with
## the tagged source.

## DOCKER_BUILDKIT used by...
export DOCKER_BUILDKIT=1

if [ "$1" != "" ]; then
  PROCESSOR_IMAGE="$1"
else
  echo Please provide target image name:version
  exit 9
fi

BUILD_IMAGE_BASE="769057607614.dkr.ecr.us-east-2.amazonaws.com/base:38"
DEPLOY_IMAGE_BASE="769057607614.dkr.ecr.us-east-2.amazonaws.com/python:3.8-slim"

docker build -t ${PROCESSOR_IMAGE} --target evaluation_image --file Dockerfile \
    --build-arg BUILD_IMAGE_SOURCE=${BUILD_IMAGE_BASE} \
    --build-arg GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS} \
    --build-arg DEPLOY_IMAGE_SOURCE=${DEPLOY_IMAGE_BASE} .