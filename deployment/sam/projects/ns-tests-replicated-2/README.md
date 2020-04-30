# SAM: ns-tests-replicated-2

This folder was created automatically by running `sam init --location generators/python --output-dir projects`. Below is a brief explanation of what we have generated for you:

```bash
.
├── README.md                   <-- This instructions file
├── BUILD                       <-- Pants BUILD file with dependencies
├── event.json                  <-- Example Lambda event payload
├── lambda_handler/             <-- Python package containing Lambda handler
│   └── lambda_handler.py       <-- Python module with Lambda handler function
├── template.yml                <-- SAM template to modify
├── build.sh                    <-- Script for building the SAM project
```

You mainly just need to make changes to:
- [`BUILD`](BUILD)
- [`lambda_handler/lambda_handler.py`](lambda_handler/lambda_handler.py)
- [`template.yml`](template.yml)

## Requirements

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://github.com/awslabs/aws-sam-cli)
- [jq](https://github.com/awslabs/aws-sam-cli)
- [Docker](https://www.docker.com/community-edition)

## Packaging and Deployment

__First, run `./build.sh`__. This will package the Lambda function, upload the artifact to S3, and generate a CloudFormation template at `/deployment/cf_templates/lambda-python-ns-tests-replicated-2.yml`.

__Second, create a development stack file__ at `/deployment/stacks/dev-talos-lambda-nstestsreplicated2.yml`. For example:
```yaml
---
component: nstestsreplicated2
environment: dev
function: lambda
name: dev-talos-lambda-nstestsreplicated2
owner: you
package: false
platform: talos
template: lambda-python-ns-tests-replicated-2.yml
```

__Third, deploy the stack with the deploy CLI:__
```bash
lexio-deploy deploy --stack-file "$TALOS_ROOT/deployment/stacks/dev-talos-lambda-nstestsreplicated2.yml"
```

When you're ready to deploy to integ or prod, create new stack files.
