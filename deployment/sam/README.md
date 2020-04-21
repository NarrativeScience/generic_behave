# Serverless Application Model (SAM) Apps

This folder contains [Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model) projects that are used to deploy Lambda functions.

## Requirements

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [AWS SAM CLI](https://github.com/awslabs/aws-sam-cli)
- [jq](https://github.com/awslabs/aws-sam-cli)
- [Docker](https://www.docker.com/community-edition)

## Layout

- __[`builder/`](./builder)__: defines a Dockerfile that's used to build Lambda function dependencies inside of an environment that mimics Amazon Linux. It's also set up to work with Pants.
- __[`generators/`](./generators)__: defines [Cookiecutter](https://github.com/audreyr/cookiecutter) templates for generating new projects
- __[`layers/`](./layers)__: containers tooling for building and deploying [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)
- __[`projects/`](./projects)__: contains SAM projects

## Usage

Generate a new project in the `projects/` directory using the following command:
```bash
sam init --location generators/<generator> --output-dir projects
```
You will be prompted to choose a name. The best practice is to use lowercase kebab-case, e.g. `new-python-project`.

Available generators:
- [__`python`__](./generators/python) (Most Common): unlocks the ability to import internal Python packages. It's a general purpose SAM project that can be used for scheduled jobs, one-off scripts, CloudFormation Custom Resources, and CloudFormation Macros to name a few. This generator has several additional prompts beyond just the project name. Check out the [Inputs](./generators/python#inputs) section for more details.
- [__`rofl`__](./generators/rofl): Request Orchestration for Lambda
