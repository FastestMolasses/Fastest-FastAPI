#!/bin/sh

### Used with Makefiles to set environment variables
### Copy this file into make-env.sh and fill in the blanks

export AWS_REGION=
export AWS_ACCOUNT_ID=
export CONTAINER_REPO_NAME=
export DOCKER_IMAGE_NAME=
export CONTAINER_NAME=
export ECS_CLUSTER_NAME=
export ECS_SERVICE_NAME=

make "$@"
