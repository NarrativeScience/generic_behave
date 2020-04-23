#!/bin/bash
# Script to compile PostgreSQL and build psycopg2 for Lambda
# Inspired by https://github.com/jkehler/awslambda-psycopg2

set -ex

echo "DOCKER_WORKING_DIR: $DOCKER_WORKING_DIR"
echo "POSTGRES_RELEASE: $POSTGRES_RELEASE"
echo "PSYCOPG2_RELEASE: $PSYCOPG2_RELEASE"
echo "PSYCOPG2_VERSION: $PSYCOPG2_VERSION"

rm -rf "$DOCKER_WORKING_DIR"
mkdir "$DOCKER_WORKING_DIR"
pushd "$DOCKER_WORKING_DIR"

curl -L "https://github.com/postgres/postgres/archive/${POSTGRES_RELEASE}.tar.gz" -O
tar xf "${POSTGRES_RELEASE}.tar.gz"
pushd "postgres-${POSTGRES_RELEASE}"
./configure --prefix "$(pwd)" --without-readline --without-zlib --with-openssl
make
make install
popd

curl -L "http://initd.org/psycopg/tarballs/${PSYCOPG2_RELEASE}/psycopg2-${PSYCOPG2_VERSION}.tar.gz" -O
tar xf "psycopg2-${PSYCOPG2_VERSION}.tar.gz"
pushd "psycopg2-${PSYCOPG2_VERSION}"
sed -i "s,pg_config.*,pg_config = ${DOCKER_WORKING_DIR}/postgres-${POSTGRES_RELEASE}/bin/pg_config,g" setup.cfg
sed -i "s,static_libpq.*,static_libpq = 1,g" setup.cfg
sed -i "s,libraries.*,libraries = ssl crypto,g" setup.cfg
python setup.py build
python setup.py bdist_wheel  # could also include sdist to generate a .tar.gz
popd

popd
