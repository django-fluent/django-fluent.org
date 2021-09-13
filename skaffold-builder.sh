#!/bin/sh
set -e

cd $(dirname $0)

# https://github.com/moby/moby/issues/42845
export DOCKER_BUILDKIT=0

export GIT_VERSION="$(git describe --tags --abbrev=0)@$(git rev-parse HEAD)"
docker build --pull --progress=tty --build-arg "GIT_VERSION=$GIT_VERSION" -t "$IMAGE" "$BUILD_CONTEXT"

if $PUSH_IMAGE; then
    docker push $IMAGE
fi
