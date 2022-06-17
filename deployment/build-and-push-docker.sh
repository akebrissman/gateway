#!/bin/bash

set -e  # Always.

BUILD=$1
DOCKER_USER=$2
DOCKER_PASSWORD=$3

BUILD_VERSION=${BUILD:-$(git rev-parse --short HEAD)}
IMAGE=abrissman/gateway-service
DOCKER_TAG=$BUILD_VERSION

echo "Log in to Docker ($DOCKER_USER)"
docker login -u $DOCKER_USER -p $DOCKER_PASSWORD
# docker pull ${IMAGE}:_base

echo "Build image"
docker build --tag ${IMAGE}:${DOCKER_TAG} --build-arg BUILD_VERSION=${BUILD_VERSION} .
echo "Built image ${IMAGE}:${DOCKER_TAG}"
# docker tag ${ID} ${IMAGE}:${BUILD_VERSION}

echo "Upload ${IMAGE}:${DOCKER_TAG}"
docker push ${IMAGE}:${DOCKER_TAG}

echo "Remove images without name"
var=$(docker images | grep "^<none>" | awk '{print $3}')
if [ -z "$var" ]
then
  echo "No images to remove"
else
  echo $var
  docker rmi --force $var
fi

docker logout

echo "Done"
