#!/bin/sh
set -e

VERSION="6.0.0b2"
MAJOR="6"

# For idempotency, remove build data or built output first
rm -rf ansible-build-data built

pip3 install --user --upgrade antsibull
git clone https://github.com/ansible-community/ansible-build-data.git
mkdir -p built collection-cache
BUILD_DATA_DIR="ansible-build-data/${MAJOR}"
BUILDFILE="ansible-${MAJOR}.build"
DEPSFILE="ansible-${VERSION}.deps"

antsibull-build rebuild-single "${VERSION}" --collection-cache collection-cache --data-dir "${BUILD_DATA_DIR}" --build-file "${BUILDFILE}" --deps-file "${DEPSFILE}" --sdist-dir built --debian

echo "The result can be found in built/ansible-${VERSION}.tar.gz"

# pip3 install --user twine
# twine upload "built/ansible-${VERSION}.tar.gz"