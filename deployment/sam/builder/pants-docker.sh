#!/bin/bash
# Helper functions for running Pants inside a Docker container

PANTS_BUILDER_IMAGE="231405699240.dkr.ecr.us-east-1.amazonaws.com/ns/talos/pants-sam-builder:latest"

BUILD_ARGS=(
  -e AWS_DEFAULT_REGION
  -e AWS_ACCESS_KEY_ID
  -e AWS_SECRET_ACCESS_KEY
  -e NPM_AUTH_TOKEN
  -v "${GENERIC_BEHAVE_ROOT}/.git:/var/task/.git"
  -v "${GENERIC_BEHAVE_ROOT}/3rdparty:/var/task/3rdparty"
  -v "${GENERIC_BEHAVE_ROOT}/apps:/var/task/apps"
  -v "${GENERIC_BEHAVE_ROOT}/db:/var/task/db"
  -v "${GENERIC_BEHAVE_ROOT}/deployment:/var/task/deployment"
  -v "${GENERIC_BEHAVE_ROOT}/dist:/var/task/dist"
  -v "${GENERIC_BEHAVE_ROOT}/lib:/var/task/lib"
  -v "${GENERIC_BEHAVE_ROOT}/pants.ini:/var/task/pants.ini"
  -v "${GENERIC_BEHAVE_ROOT}/pants:/var/task/pants"
  -v "${GENERIC_BEHAVE_ROOT}/servers:/var/task/servers"
  -v "${GENERIC_BEHAVE_ROOT}/stepfunctions:/var/task/stepfunctions"
  -v "${GENERIC_BEHAVE_ROOT}/src:/var/task/src"
  -v "${GENERIC_BEHAVE_ROOT}/tests_replicated:/var/task/tests_replicated"
  "$PANTS_BUILDER_IMAGE"
)

function pants-shell() {
  (
    docker run -it --rm --name sam $@ ${BUILD_ARGS[@]} bash
  )
}

function pants-run() {
  (
    local cmd=$@
    if [[ -z "$(docker ps -f 'name=sam' -q)" ]]; then
      # Run in a new ephemeral container
      docker run --rm ${BUILD_ARGS[@]} ./pants ${cmd[@]}
    else
      # Run in the existing container named sam
      docker exec sam ./pants ${cmd[@]}
    fi
  )
}
