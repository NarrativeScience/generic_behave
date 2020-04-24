"""Generic steps for accessing aws buckets"""
import json
import logging

from behave import given, use_step_matcher, when
from behave.runner import Context
import boto3

LOGGER = logging.getLogger(__name__)

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


@given(
    "the (?P<request_type>JSON|json|tarball) request data from the (?P<bucket>[-\d\w_]+) S3 bucket at the path (?P<key_path>[-\d\w/._]+)"
)
def retrieve_s3_payload(
    ctx: Context, request_type: str, bucket: str, key_path: str
) -> None:
    """Retrieve JSON data from an aws s3 bucket and set as the request data

    Args:
        ctx: The behave context
        request_type: The type of data to send
        bucket: The s3 bucket containing the JSON request data
        key_path: The path to the data in aws

    """
    LOGGER.debug(f"Attempting to retrieve data from {bucket}/{key_path}")
    s3 = boto3.client("s3")
    payload = s3.get_object(Bucket=bucket, Key=key_path)
    LOGGER.debug(f"Successfully retrieved data from {bucket}/{key_path}")
    if request_type in ("JSON", "json"):
        ctx.request_data = json.loads(payload["Body"].read().decode())
    else:
        ctx.request_data = payload["Body"].read()


@when(
    "the JSON request data is sent to the (?P<bucket>[-\d\w_]+) S3 bucket at the path (?P<key_path>[-\d\w/._]+)"
)
def send_s3_payload(ctx: Context, bucket: str, key_path: str) -> None:
    """Send JSON data to an aws s3 bucket

    Args:
        ctx: The behave context
        bucket: The s3 bucket containing the
        key_path: The path to the data in aws

    """
    LOGGER.debug(f"Attempting to send data to {bucket}/{key_path}")
    s3 = boto3.client("s3")
    ctx.response = s3.put_object(Body=ctx.request_data, Bucket=bucket, Key=key_path)
    LOGGER.debug(f"Successfully sent data to {bucket}/{key_path}")
