# Pants SAM Builder

This Docker container image mimics Amazon Linux (the AWS Lambda OS) and has Pants preinstalled. The Dockerfile is mostly a copy of the [lambci/lambda](https://hub.docker.com/r/lambci/lambda):python3.6 [Dockerfile](https://github.com/lambci/docker-lambda/blob/master/python3.6/build/Dockerfile) except that it compiles Python with sqlite support that Pants requires.

## Build and Publish
```bash
docker build \
  -t 231405699240.dkr.ecr.us-east-1.amazonaws.com/ns/talos/pants-sam-builder:latest \
  -f deployment/sam/builder/Dockerfile \
  $TALOS_ROOT
docker push 231405699240.dkr.ecr.us-east-1.amazonaws.com/ns/talos/pants-sam-builder:latest
```

## Helpers
If you're working with the Pants SAM builder a lot, you can speed up Pants commands by keeping a Docker container running so the build cache sticks around:
```bash
source "$TALOS_ROOT/deployment/sam/builder/pants-docker.sh"
pants-shell
```
This will launch a container named `sam`. Various calls to run Pants inside of a container will prefer to use this running container over launching an ephemeral one.
