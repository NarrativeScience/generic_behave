"""Generic step definitions for behave debugging"""

import logging
import pdb
from pprint import pformat

from behave import step, use_step_matcher
from behave.runner import Context
from ns_behave.common.common_behave_functions import CommonBehave

# Enable the regex step matcher for behave in this class
use_step_matcher("re")

# Set up a logger
LOGGER = logging.getLogger("behave-debug")


@step("set pdb")
def step_debug_pdb(ctx: Context) -> None:
    """Sets a pdb to be used for debugging.

    The gherkin-linter will catch this step to prevent a pdb being pushed.
    Multiple if statements log everything a dev would need to start debugging the issue.

    Args:
        ctx: The behave context object

    """
    LOGGER.debug(
        "Behave PDB step was set. Current context attributes broken down by context layer:"
    )
    CommonBehave.log_context_attributes(ctx)
    pdb.set_trace()


@step(
    "(?i)the request (?P<content>data|headers) are logged(?: as (?P<log_level>info|debug))?"
)
def step_log_request_data(ctx: Context, content: str, log_level: str = "debug") -> None:
    """Logs the request data from the behave context

        Args:
            ctx: The behave context
            content: The type of content to log (headers or data)
            log_level: A string representing the level of logging to use

        """
    content = "request_data" if content == "data" else content
    try:
        if hasattr(ctx, content):
            LOGGER.info(
                pformat(getattr(ctx, content))
            ) if log_level == "info" else LOGGER.debug(pformat(getattr(ctx, content)))
        else:
            LOGGER.info("No response has been saved to the behave context.")
    except Exception as error:
        LOGGER.info(f"Exception raised: {error}")


@step(
    "(?i)the (?P<response_type>JSON|text) response is logged(?: as (?P<log_level>info|debug))?"
)
def step_log_response(
    ctx: Context, response_type: str, log_level: str = "debug"
) -> None:
    """Logs the response from the behave context

    Args:
        ctx: The behave context
        response_type: The type of response to print
        log_level: A string representing the level of logging to use

    """
    try:
        if hasattr(ctx, "response"):
            if response_type.upper() == "JSON":
                response = pformat(ctx.response.json())
            else:
                response = ctx.response
            LOGGER.info(response) if log_level == "info" else LOGGER.debug(response)
        else:
            LOGGER.info("No response has been saved to the behave context.")
    except Exception as error:
        LOGGER.info(f"Exception raised: {error}")
