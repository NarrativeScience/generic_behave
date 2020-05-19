#!/bin/bash
# Helper functions for working with SAM projects created by the "python" generator

if [[ -z "$GENERIC_BEHAVE_ROOT" ]]; then
  echo "Missing required environment variable: GENERIC_BEHAVE_ROOT"
  exit 1
fi

if [[ ! $(which jq) ]]; then
  echo "ERROR: missing jq. Please install: https://stedolan.github.io/jq/download/"
  exit 1
fi

source "$GENERIC_BEHAVE_ROOT/deployment/sam/builder/pants-docker.sh"

ACCOUNT_ID=$(aws sts get-caller-identity  | jq '.Account' | sed "s/\"//g")

if [[ $ACCOUNT_ID == "231405699240" ]]; then
    S3_BUCKET="serverless-231405699240"
else
    S3_BUCKET="$ACCOUNT_ID.serverless"
fi

# Build a Python Lambda function using the Docker builder image
function sam-python-build() {
  (
    set -e

    local sam_project="$(echo "$1" | jq -r .project_name -)"

    echo "Cleaning out existing PEX files"
    rm -f $(find "${GENERIC_BEHAVE_ROOT}/dist" -name "lambda-python-${sam_project}*")

    echo "Creating Lambda bundle"
    pants-run bundle \
      --cache-binary-py-ignore \
      --cache-bundle-py-ignore \
      --cache-bundle-lambdex-prep-ignore \
      --cache-bundle-lambdex-run-ignore \
      "deployment/sam/projects/${sam_project}:lambda-python-${sam_project}"

    echo "Setting file permissions in Lambda bundle"
    local dist="${GENERIC_BEHAVE_ROOT}/dist/lambda-python-${sam_project}.pex"
    local tmpdir="$(mktemp -d)"
    pushd "$tmpdir" > /dev/null
    unzip -qo "$dist"
    chmod -R 755 .
    zip -rmq "lambda-python-${sam_project}" * .[^.]*
    mv "lambda-python-${sam_project}.zip" "$dist"
    popd > /dev/null
  )
}

# Publish the PEX file to S3 and update the CodeUri property in the CF template
function sam-python-publish() {
  (
    set -e

    local sam_project="$(echo "$1" | jq -r .project_name -)"
    local is_nested_stack="$(echo "$1" | jq -r .is_nested_stack -)"
    local lambda_function_pex_file="${GENERIC_BEHAVE_ROOT}/dist/lambda-python-${sam_project}.pex"
    local checksum="$(sha256sum < "$lambda_function_pex_file" | cut -d' ' -f1)"
    local code_uri="s3://${S3_BUCKET}/${checksum}"
    local cf_template_name="lambda-python-${sam_project}.yml"
    local cf_template_path
    if [[ "$is_nested_stack" == "yes" ]]; then
      cf_template_path="${GENERIC_BEHAVE_ROOT}/deployment/cf_templates/nested-stacks/${cf_template_name}"
    else
      cf_template_path="${GENERIC_BEHAVE_ROOT}/deployment/cf_templates/${cf_template_name}"
    fi

    echo "Uploading Lambda bundle to S3"
    aws s3 cp "$lambda_function_pex_file" "$code_uri"

    local generate_cf_template="$(echo "$1" | jq -r .generate_cf_template -)"
    if [[ -z "$generate_cf_template" || "$generate_cf_template" == "null" || "$generate_cf_template" == "yes" ]]; then
      echo "Copying CloudFormation template and setting CodeUri"
      sam validate
      cp template.yml "$cf_template_path"
      if [[ "$(uname)" == "Linux" ]]; then
        sed -i "s,__CODE_URI__,${code_uri},g" "$cf_template_path"
      else
        sed -i '' "s,__CODE_URI__,${code_uri},g" "$cf_template_path"
      fi
      echo "Ready to commit and merge $cf_template_path"
    else
      echo "Skipping CloudFormation template generation"
    fi
  )
}
