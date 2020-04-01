"""A thin wrapper around the LaunchDarkly APIs to use as a test SDK

This wrapper will allow a user to:
- Get global flag value
- Get flag value for a user
- Update global flag value
- Update flag value for a user
"""
import logging

from ns_requests.generic_requests import GenericRequests
from requests import Session

# Initialize a logger
LOGGER = logging.getLogger(__name__)

# Global Variables
LD_BASE_URL = "https://app.launchdarkly.com/api/v2"


class FeatureFlagSDK:
    """Wrapper that holds all wrapped LaunchDarkly functions to call APIs"""

    @staticmethod
    def get_flag_value(
        project_key: str, environment: str, auth_token: str, feature_flag_key: str
    ) -> bool:
        """Get the default feature flag value in an environment

        Args:
            project_key: LaunchDarkly project key. ie. default, talos, etc
            environment: LaunchDarkly environment key. ie. integ, production, circleci
            auth_token: LaunchDarkly API auth key
            feature_flag_key: The flag key to update

        Returns:
            The feature flag value for the global settings without targeting

        """
        LOGGER.debug(f"Attempting to get default value for flag: {feature_flag_key}")
        response = GenericRequests.get_request(
            Session(),
            url=f"{LD_BASE_URL}/flag-statuses/{project_key}/{environment}/{feature_flag_key}",
            headers={"Authorization": auth_token},
        )
        if response.status_code != 200:
            LOGGER.error(f"Unable to retrieve feature flag: '{feature_flag_key}'")
            LOGGER.error(f"Response: {response.text}")
            exit(1)
        else:
            # check to make sure flag is active and has a default value being served
            if "default" in response.json():
                flag_value = response.json()["default"]
                LOGGER.debug(
                    f"Feature flag successfully retrieved: '{feature_flag_key}: {flag_value}'"
                )
                return flag_value
            else:
                LOGGER.error(
                    f"Could not find default value in the flag status. "
                    f"Check the LaunchDarkly configuration for {feature_flag_key}"
                )
                LOGGER.error(f"Response: {response.text}")
                exit(1)

    @staticmethod
    def update_flag(
        project_key: str,
        environment: str,
        auth_token: str,
        feature_flag_key: str,
        flag_value: bool,
    ) -> dict:
        """Update a global feature flag value for a given flag

        Args:
            project_key: LaunchDarkly project key. ie. default, talos, etc
            environment: LaunchDarkly environment key. ie. integ, production, circleci
            auth_token: LaunchDarkly API auth key
            feature_flag_key: The flag key to update
            flag_value: The value to set the flag to

        """
        LOGGER.debug(
            f"Attempting to update default value for feature flag: {feature_flag_key} with value: {flag_value}"
        )
        response = GenericRequests.patch_request(
            Session(),
            url=f"{LD_BASE_URL}/flags/{project_key}/{feature_flag_key}",
            headers={"Authorization": auth_token},
            json=[
                {
                    "op": "replace",
                    "path": f"/environments/{environment}/{feature_flag_key}",
                    "value": flag_value,
                }
            ],
        )
        if response.status_code != 200:
            LOGGER.error(f"Unable to update feature flag: '{feature_flag_key}'")
            LOGGER.error(f"Response: {response.text}")
            exit(1)
        else:
            LOGGER.debug(
                f"Feature flag successfully updated: {feature_flag_key} value: {flag_value}"
            )
            return response.json()

    @staticmethod
    def get_flag_value_for_user(
        project_key: str,
        environment: str,
        auth_token: str,
        user_id: str,
        feature_flag_key: str,
    ) -> bool:
        """Get a feature flag value for a given user

        Args:
            project_key: LaunchDarkly project key. ie. default, talos, etc
            environment: LaunchDarkly environment key. ie. integ, production, circleci
            auth_token: LaunchDarkly API auth key
            user_id: The user ID of the user
            feature_flag_key: The flag key to get the value of

        Returns:
            The boolean value of the feature flag status for given user

        """
        LOGGER.debug(
            f"Attempting to get feature flag value for flag: {feature_flag_key} user: {user_id}"
        )
        response = GenericRequests.get_request(
            Session(),
            url=f"{LD_BASE_URL}/users/{project_key}/{environment}/{user_id}/flags/{feature_flag_key}",
            headers={"Authorization": auth_token},
        )
        if response.status_code != 200:
            LOGGER.error(
                f"Unable to retrieve feature flag: {feature_flag_key} for user: {user_id}"
            )
            LOGGER.error(f"Response: {response.text}")
            exit(1)
        else:
            # Check to make sure the value of the flag is present and return it
            if "_value" in response.json():
                flag_value = response.json()["_value"]
                LOGGER.debug(
                    f"Successfully retrieved feature flag: {feature_flag_key} value: {flag_value} for user: {user_id}"
                )
                return flag_value
            else:
                LOGGER.error(
                    f"Could not find feature flag value: {feature_flag_key} for user: {user_id}"
                )
                LOGGER.error(f"Response: {response.text}")
                exit(1)

    @staticmethod
    def update_flag_value_for_user(
        project_key: str,
        environment: str,
        auth_token: str,
        user_id: str,
        feature_flag_key: str,
        flag_value: bool,
    ) -> None:
        """Update a feature flag value for a given user

        Args:
            project_key: LaunchDarkly project key. ie. default, talos, etc
            environment: LaunchDarkly environment key. ie. integ, production, circleci
            auth_token: LaunchDarkly API auth key
            user_id: The user ID of the user
            feature_flag_key: The flag key to get the value of
            flag_value: The value to update to

        """
        LOGGER.debug(
            f"Attempting to update a feature flag: {feature_flag_key} with value: {flag_value} for user: {user_id}"
        )
        response = GenericRequests.put_request(
            Session(),
            url=f"{LD_BASE_URL}/users/{project_key}/{environment}/{user_id}/flags/{feature_flag_key}",
            headers={"Authorization": auth_token},
            json={"setting": flag_value},
        )
        if response.status_code != 204:
            LOGGER.error(
                f"Unable to update feature flag: {feature_flag_key} with value: {flag_value} for user: {user_id}"
            )
            LOGGER.error(f"Response: {response.text}")
            exit(1)
        else:
            LOGGER.debug(
                f"Feature flag successfully updated: {feature_flag_key} with value: {flag_value} for user: {user_id}"
            )
