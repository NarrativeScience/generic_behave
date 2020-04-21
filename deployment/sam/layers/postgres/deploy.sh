#!/bin/bash

set -e

ENVIRONMENT="${1:-dev}"
LAYER_NAME="${ENVIRONMENT}-talos-lambdalayer-postgres"
S3_BUCKET=serverless-231405699240
S3_KEY="_layers/${LAYER_NAME}.zip"
S3_PATH="s3://${S3_BUCKET}/${S3_KEY}"

# Upload to S3 for importing into Lambda
aws s3 cp layer.zip "$S3_PATH"

# Publish new layer version
aws lambda publish-layer-version \
  --layer-name "$LAYER_NAME" \
  --content "S3Bucket=${S3_BUCKET},S3Key=${S3_KEY}"
