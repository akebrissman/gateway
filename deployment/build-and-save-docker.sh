#!/bin/bash

set -e  # Always.

BUILD=$1

BUILD_VERSION=${BUILD:-$(git rev-parse --short HEAD)}
IMAGE=abrissman/gateway-service
# DOCKER_TAG=BUILD_VERSION
DOCKER_TAG=local-build

# docker login -u foo -p pwd <server>

if [[ $(command -v pigz ) ]]; then
    echo "DEBUG: Using pigz for compression."
    COMP_CMD=pigz
else
    echo "DEBUG: Resorting to plain gzip compression."
    COMP_CMD=gzip
fi

# docker pull gateway-service:_base

docker build -f Dockerfile \
    -t ${IMAGE}:${DOCKER_TAG} \
    --build-arg BUILD_VERSION=${BUILD_VERSION} .

mkdir -p build

docker save ${IMAGE}:${DOCKER_TAG} \
    | $COMP_CMD - > build/gateway-service-${BUILD_VERSION}.tar.gz
