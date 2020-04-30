#!/bin/bash
set -e

if [[ -z "$TALOS_ROOT" ]]; then
  echo "Missing required environment variable: TALOS_ROOT"
  exit 1
fi

source "$TALOS_ROOT/deployment/sam/generators/python/helpers.sh"
CONFIG="$(cat .generator.json)"
sam-python-build "$CONFIG"
sam-python-publish "$CONFIG"
