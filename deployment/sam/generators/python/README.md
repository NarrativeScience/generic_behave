# Cookiecutter Project for a Python SAM Project

A [Cookiecutter](https://github.com/audreyr/cookiecutter) template to create a boilerplate project using [Serverless Application Model (SAM)](https://github.com/awslabs/serverless-application-model). This project is for deploying Python code to a Lambda function.

## Inputs
When you create a new SAM project with this Cookiecutter template, you will be prompted to enter these inputs:

Input | Default | Description
--- | --- | ---
`project_name` | `new-python-project` | Name of the SAM project. This should be a meaningful, semantic name. Use kebab-case.
`requires_vpc` | `yes` | Whether the Lambda function requires VPC access. You should choose `yes` if you need direct access to an AWS resource in the VPC, like an RDS database. If you're writing something like a CloudFormation Macro or script that curls an endpoint, choose `no`. Options: `yes`, `no`
`requires_dlq` | `yes` | Whether to create a dead-letter queue (DLQ) and associated CloudWatch alarm for the Lambda function. This is useful if you want failed Lambda invocations to be tracked and retried. If you don't care if the Lambda function fails (e.g. if another one will trigger soon after) then choose `no`. Options: `yes`, `no`
`requires_postgres` | `yes` | Whether to add a Lambda Layer to the Function configuration that provides native PostgreSQL dependencies. Choose `yes` if you need to query a Postgres database with a library like psycopg2, aiopg, etc. Options: `yes`, `no`
`is_nested_stack` | `no` | Whether the CloudFormation stack that we generate should be placed in the [`nested-stacks` folder](/deployment/cf_templates/nested-stacks). If this Lambda function is independent of the main application (e.g. it's a CloudFormation Macro), choose `no`. Options: `yes`, `no`
`is_cf_custom_resource` | `no` | Whether the Lambda Function will be used as a CloudFormation Custom Resource handler. If you choose `yes`, the `lambda_handler.py` will include boilerplate for a new handler class. Options: `yes`, `no`

## Updating the Cookiecutter Project

### Adding new variables
1. Add a variable to the Cookiecutter configuration file: [`cookiecutter.json`](./cookiecutter.json).
    - The variable name should be snake_case
    - If defining a choice variable, put the default option first in the list
    - Note that values are interpreted as strings so use `["yes", "no"]` for boolean options
1. Update the `.generator.json` file with the new variable. This file is how we track what values the user provided when they used the generator. Unless the change to the template is major, leave the version at 1.
1. Update the relevant files and folders to use your new template variable. For docs on what you can do, check out [Jinja](https://jinja.palletsprojects.com/en/2.10.x/).
1. Test out your changes by running `sam init -l generators/python -o projects`
