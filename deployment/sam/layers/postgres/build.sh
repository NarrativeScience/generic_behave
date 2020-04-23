#!/bin/bash

set -e

POSTGRES_RELEASE=REL_10_9
PSYCOPG2_RELEASE=PSYCOPG-2-8
PSYCOPG2_VERSION=2.8.3
DOCKER_CONTAINER=sam
DOCKER_WORKING_DIR=/tmp/layer
COMPILE_SCRIPT=compile.sh
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
pushd "$DIR"

# Copy the script into the container
docker cp "${DIR}/compile.sh" "${DOCKER_CONTAINER}:/tmp/${COMPILE_SCRIPT}"
docker exec \
  -e "DOCKER_WORKING_DIR=${DOCKER_WORKING_DIR}" \
  -e "POSTGRES_RELEASE=${POSTGRES_RELEASE}" \
  -e "PSYCOPG2_RELEASE=${PSYCOPG2_RELEASE}" \
  -e "PSYCOPG2_VERSION=${PSYCOPG2_VERSION}" \
  "${DOCKER_CONTAINER}" \
  "/tmp/${COMPILE_SCRIPT}"

# Copy the distribution files (.whl) out of the container
rm -rf dist
docker cp \
  "${DOCKER_CONTAINER}:${DOCKER_WORKING_DIR}/psycopg2-${PSYCOPG2_VERSION}/dist/" \
  dist

# Copy the libpq header files out of the container
rm -rf lib
mkdir lib
for f in libpq.so libpq.so.5 libpq.so.5.10; do
  docker cp \
    "${DOCKER_CONTAINER}:${DOCKER_WORKING_DIR}/postgres-${POSTGRES_RELEASE}/lib/${f}" \
    lib/
done

# Download RDS and Redshift SSL certificates
wget -O lib/rds-combined-ca-bundle.pem https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
wget -O lib/rds-ca-2019-root.pem https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem
wget -O lib/redshift-ca-bundle.crt https://s3.amazonaws.com/redshift-downloads/redshift-ca-bundle.crt

# Create the layer artifact (zip file)
rm -f layer.zip
zip -r layer.zip lib

popd
