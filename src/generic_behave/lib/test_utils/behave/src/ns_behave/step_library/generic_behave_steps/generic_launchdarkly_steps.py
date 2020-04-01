"""Generic step definitions for interfacing with LaunchDarkly"""

import logging

from behave import given, step, use_step_matcher
from behave.runner import Context
from ns_behave.common.common_behave_functions import CommonBehave
from ns_launchdarkly.feature_flag_sdk import FeatureFlagSDK

# Enable the regex step matcher for behave in this class
use_step_matcher("re")
# Set up a logger
LOGGER = logging.getLogger(__name__)


@step(
    'the value of (?:the | )?"(?P<feature_flag_key>.*)" feature flag(?: for "(?P<user_id>.*)")? is logged'
)
def step_print_flag_status_user(
    ctx: Context, feature_flag_key: str, user_id: str = None
) -> None:
    """Get the value of a specific feature flag for a given user and log it

    Args:
        ctx: The behave context
        feature_flag_key: The key of the flag to get value of
        user_id: The user ID of the user

    """
    if ctx.environment not in ["dev", "prod"]:
        user_id = CommonBehave.interpolate_context_attributes(ctx, user_id)
        if user_id:
            flag_value = FeatureFlagSDK.get_flag_value_for_user(
                ctx.ld_project_key,
                ctx.ld_environment,
                ctx.ld_auth_token,
                user_id,
                feature_flag_key,
            )
        else:
            flag_value = FeatureFlagSDK.get_flag_value(
                ctx.ld_project_key,
                ctx.ld_environment,
                ctx.ld_auth_token,
                feature_flag_key,
            )
        LOGGER.info(
            f'Feature flag: {feature_flag_key} value: {flag_value} user: {user_id if user_id else "global"}'
        )
        LOGGER.info("")
    else:
        LOGGER.warning(
            f"LaunchDarkly flag operations are not available in the {ctx.environment} environment. "
            f"Please manually set the flag in the ns_python_core.config.py and re-run your test."
        )


@given(
    'the "(?P<feature_flag_key>.*)" feature flag is (?P<flag_operation>enabled|disabled)(?: for "(?P<user_id>.*)?")?'
)
def step_update_feature_flag(
    ctx: Context, feature_flag_key: str, flag_operation: str, user_id: str = None
) -> None:
    """Update the value of a feature flag for a user

    Args:
        ctx: The behave context
        feature_flag_key: The key of the flag to set value of
        flag_operation: Either enable or disable the flag
        user_id: The user ID of the user

    """
    if ctx.environment not in ["dev", "prod"]:
        user_id = CommonBehave.interpolate_context_attributes(ctx, user_id)
        flag_value = True if flag_operation == "enabled" else False
        if user_id:
            FeatureFlagSDK.update_flag_value_for_user(
                ctx.ld_project_key,
                ctx.ld_environment,
                ctx.ld_auth_token,
                user_id,
                feature_flag_key,
                flag_value,
            )
        else:
            FeatureFlagSDK.update_flag(
                ctx.ld_project_key,
                ctx.ld_environment,
                ctx.ld_auth_token,
                feature_flag_key,
                flag_value,
            )
    else:
        LOGGER.warning(
            f"LaunchDarkly flag operations are not available in the {ctx.environment} environment. "
            f"Please manually set the flag in the ns_python_core.config.py and re-run your test."
        )
