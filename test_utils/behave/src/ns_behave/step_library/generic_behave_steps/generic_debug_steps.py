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


@step("(?i)the JSON response is logged(?: as (?P<log_level>info|debug))?")
def step_log_response(ctx: Context, log_level: str = "debug") -> None:
    """Logs the JSON response from the behave context

    Args:
        ctx: The behave context
        log_level: A string representing the level of logging to use

    """
    try:
        if hasattr(ctx, "response"):
            LOGGER.info(
                pformat(ctx.response.json())
            ) if log_level == "info" else LOGGER.debug(pformat(ctx.response.json()))
        else:
            LOGGER.info("No response has been saved to the behave context.")
    except Exception:
        LOGGER.info("Response is not of type JSON.")
