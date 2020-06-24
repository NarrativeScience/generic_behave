"""
Step definitions for Replicated tests
"""
import logging
import requests
import boto3
import json
import time
from jsonpath import jsonpath
from ns_behave.common.common_behave_functions import CommonBehave

from behave import given, then, when, use_step_matcher
from behave.runner import Context

from ns_behave.step_library.generic_behave_steps import generic_assert_steps

# Enable the regex step matcher for behave in this class
use_step_matcher("re")
# Set up a logger
LOGGER = logging.getLogger(__name__)


@given("a version request is sent to the replicated test stack")
def request_version(ctx: Context) -> None:
    LOGGER.debug('Attempting to send a version request to the replicated test stack')
    ctx.response = requests.Session().request(
        method="get", url=ctx.gateway_base_url, verify=False
    )
    response = ctx.response.text
    LOGGER.debug(f"Successfully sent a version request to the replicated test stack with response: {response}")


@then('the replicated test server is polled (?P<wait_time>\d+) times to detect the version change')
def validate_version(ctx: Context, wait_time: int):
    LOGGER.debug(f'Polling the replicated test server for {wait_time} minutes to verify version change to {ctx.viz_version}.')
    wait_time = int(wait_time)
    while wait_time > 0:
        if str(jsonpath(ctx.response.json(), CommonBehave.interpolate_context_attributes(ctx, "version"))[0]) == ctx.viz_version:
            LOGGER.debug(f'Quill version {ctx.viz_version} detected.  Continuing test suite.')
            break
        else:
            LOGGER.debug(f'Version {jsonpath(ctx.response.json(), CommonBehave.interpolate_context_attributes(ctx, "version"))} detected.  Polling again in 30 seconds.')
            time.sleep(30)
        wait_time -= 1
    generic_assert_steps.step_assert_rest_response_value(ctx, "version", None, ctx.viz_version)


@given('the test data is retrieved from S3')
def retrieve_s3_payload(ctx: Context) -> None:
    s3 = boto3.client('s3')
    payload = s3.get_object(Bucket='s3-ns-viz', Key='datasets/regression-datasets/Scatterplot/v2_scatterplot_2M.json')
    ctx.request_data = json.loads(payload["Body"].read().decode())
    LOGGER.debug(ctx.request_data)


@when('a story request is sent to (?P<url>.*)')
def request_story(ctx: Context, url: str) -> None:
    LOGGER.debug(f'Attempting to send a story request to {url}')
    ctx.response = requests.Session().request(
        method="post", url=ctx.gateway_base_url + url, verify=False, json=ctx.request_data
    )
    response = ctx.response.text
    LOGGER.debug(f"Successfully sent a story request with response: {response}")


@given('the viz extension (?P<extension>.*) is polled')
def poll_extension(ctx: Context, extension: str) -> None:
    LOGGER.debug(f'Attempting poll viz extension: {extension}')
    ctx.response = requests.Session().request(
        method="get", url='{}v1/extensions/{}/static/main.js'.format(ctx.gateway_base_url, extension), verify=False
    )
    LOGGER.debug(f'Successfully polled viz extension: {extension}')
