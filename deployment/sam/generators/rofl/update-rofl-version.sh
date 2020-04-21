#!/bin/bash
# Update the rofl package version in the generator and optionally in all projects that
# used the generator.
#
# Usage:
#
#   ./update-rofl-version.sh
#
# Requirements:
#   * Node.js 10 installed and activated in the shell prior to running this script
#   * jq installed

set -e

SAM_DIR="$TALOS_ROOT/deployment/sam"
GENERATOR_DIR="$SAM_DIR/generators/rofl"
GENERATOR_PACKAGE_DIR="$GENERATOR_DIR/{{cookiecutter.project_name}}/package"

read -p "What rofl version do you want to install? (Default: latest): " -r
VERSION=${REPLY:-latest}

echo "Updating the generator"
pushd "$GENERATOR_PACKAGE_DIR" > /dev/null
npm install --save "@narrativescience/rofl@$VERSION"
rm -rf node_modules/
popd > /dev/null

read -p "Do you want to update ALL existing rofl projects with this new version? (y) or (n): " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  pushd "$SAM_DIR" > /dev/null
  for dir in ./*/; do
    project_folder="$(basename "$dir")"
    if [[ "$project_folder" != "generators" ]]; then
      generator="$(jq -r .generator "./$project_folder/.generator.json")"
      if [[ "$generator" == "rofl" ]]; then
        echo "Updating $project_folder"
        pushd "$project_folder/package" > /dev/null
        npm install --save "@narrativescience/rofl@$VERSION"
        popd > /dev/null
      fi
    fi
  done
  popd > /dev/null
fi

echo "Complete. Make sure to commit the files that were just modified."
