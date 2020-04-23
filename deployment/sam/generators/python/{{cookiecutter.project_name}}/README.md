{%- set component = cookiecutter.project_name | lower | replace("_", "") | replace("-", "") -%}
# SAM: {{ cookiecutter.project_name }}

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

__First, run `./build.sh`__. This will package the Lambda function, upload the artifact to S3, and generate a CloudFormation template at `/deployment/cf_templates/{% if cookiecutter.is_nested_stack == "yes" %}nested-stacks/{% endif %}lambda-python-{{ cookiecutter.project_name }}.yml`.

{% if cookiecutter.is_nested_stack == "yes" -%}
To deploy the stack along with our normal CI/CD pipeline, __add the nested stack as a resource in the main `talos-application.yml` CF template__. For example:
```yaml
MyNewSAMStack:
  Type: AWS::CloudFormation::Stack
  Properties:
    TemplateURL: ./nested-stacks/lambda-python-{{ cookiecutter.project_name }}.yml
    Parameters:
      Environment: !Ref Environment
      Platform: !Ref Platform
      Function: !Ref Function
    TimeoutInMinutes: 60
    Tags:
      - Key: Environment
        Value: !Ref Environment
      - Key: Platform
        Value: !Ref Platform
      - Key: Function
        Value: !Ref Function
```
{% else -%}
__Second, create a development stack file__ at `/deployment/stacks/dev-talos-lambda-{{ component }}.yml`. For example:
```yaml
---
component: {{ component }}
environment: dev
function: lambda
name: dev-talos-lambda-{{ component }}
owner: you
package: false
platform: talos
template: lambda-python-{{ cookiecutter.project_name }}.yml
```

__Third, deploy the stack with the deploy CLI:__
```bash
lexio-deploy deploy --stack-file "$TALOS_ROOT/deployment/stacks/dev-talos-lambda-{{ component }}.yml"
```

When you're ready to deploy to integ or prod, create new stack files.
{% endif -%}
