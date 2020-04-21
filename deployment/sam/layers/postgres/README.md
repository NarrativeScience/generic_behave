# Lambda Layer: Postgres

This Layer provides native Postgres header files to the Lambda Function. This is needed by libraries like psycopg2 and aiopg.

A currently running [SAM builder](../builder) Docker container can be used to download PostgreSQL, compile it from source with certain flags, then extract the `libpq.so` header files to package into a Lambda layer. While we're at it we also build the psycopg2 library from source to ensure it uses the right headers.

First, it's a good idea to launch a shell for the SAM builder in a separate terminal:
```bash
source "${TALOS_ROOT}/deployment/sam/builder/pants-docker.sh"
pants-shell
```

To build a new layer artifact (.zip file), run:
```bash
./build.sh
```
This generates a new `layer.zip` file with the `libpq.so` files as well as `dist/psycopg2-*.whl`.

To deploy a new Layer version, run:
```bash
./deploy.sh <environment>
```
where `<environment>` is either `dev` or `prod`.

Deploying the Layer will output something like:
```
upload: ./layer.zip to s3://serverless-231405699240/_layers/prod-talos-lambdalayer-postgres.zip
{
    "Content": {
        "Location": "https://...",
        "CodeSha256": "...",
        "CodeSize": 123
    },
    "LayerArn": "arn:aws:lambda:us-east-1:231405699240:layer:prod-talos-lambdalayer-postgres",
    "LayerVersionArn": "arn:aws:lambda:us-east-1:231405699240:layer:prod-talos-lambdalayer-postgres:1",
    "Description": "",
    "CreatedDate": "2019-07-03T22:09:37.051+0000",
    "Version": 1
}
```
Grab the new `LayerVersionArn` value and update the `Layers` list in your SAM project's `template.yml`, e.g.:
```yaml
Layers:
  - !If
      - Production
      - arn:aws:lambda:us-east-1:231405699240:layer:prod-talos-lambdalayer-postgres:1
      - arn:aws:lambda:us-east-1:231405699240:layer:dev-talos-lambdalayer-postgres:1
```

Before building a SAM Python project, you should copy the new `dist/psycopg2-*.whl` file to the [`/3rdparty/python/repo/`](/3rdparty/python/repo/) folder. This serves as a simple Python Package Repository for Pants to look at when installing packages.
