"""Common REST Authentication and client creation steps"""

import logging

from behave import given, use_step_matcher
from behave.runner import Context
from ns_behave.common.common_behave_functions import CommonBehave

# Enable the regex step matcher
use_step_matcher("re")

# Setup a logger
LOGGER = logging.getLogger(__name__)


@given(
    "the (?i)(?P<role_type>site_admin|org_admin|org_member|unauthorized) client(?: and (?P<is_user>|user))?"
)
def step_auth_request_client(ctx: Context, role_type: str, is_user: str) -> None:
    """Sets the client and user_id on the behave context so we have proper authentication for the user making the request.

    If no client is found on the context for that user we will create a user and a client for that user.

    Args:
        ctx: The behave context
        role_type: The user role to search for a client for and set
        is_user: A flag to know if we want to set the role_type as the current user

    """
    LOGGER.debug(f"Attempting to set the request client for the '{role_type}' user")
    if role_type in ("site_admin", "org_admin", "org_member"):
        ctx.client = CommonBehave.get_test_user_client(ctx, role_type)
        if is_user:
            ctx.user_id = CommonBehave.get_test_user_id(ctx, role_type)
    else:
        ctx.client = None
    LOGGER.debug(f"The client was set successfully for the {role_type} user")
