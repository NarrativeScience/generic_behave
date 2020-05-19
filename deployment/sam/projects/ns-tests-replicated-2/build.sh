#!/bin/bash
set -e

if [[ -z "$GENERIC_BEHAVE_ROOT" ]]; then
  echo "Missing required environment variable: GENERIC_BEHAVE_ROOT"
  exit 1
fi

source "$GENERIC_BEHAVE_ROOT/deployment/sam/generators/python/helpers.sh"
CONFIG="$(cat .generator.json)"
sam-python-build "$CONFIG"
sam-python-publish "$CONFIG"
