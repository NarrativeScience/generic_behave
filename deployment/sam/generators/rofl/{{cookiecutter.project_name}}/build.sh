#!/bin/bash
set -e

if [[ -z "$TALOS_ROOT" ]]; then
  echo "Missing required environment variable: TALOS_ROOT"
  exit 1
fi

# Builds the AWS Lambda Functions source code to generate artifacts that target AWS
# Lambda's execution environment
sam build

# The SAM package command creates a zip of your code and dependencies and
# uploads it to S3. The command returns a copy of your template, replacing
# references to local artifacts with the S3 location where the command
# uploaded the artifacts.
sam package \
  --s3-bucket "{{ cookiecutter.s3_bucket }}" \
  --output-template-file "$TALOS_ROOT/deployment/cf_templates/nested-stacks/rofl-{{ cookiecutter.project_name }}.yml"
