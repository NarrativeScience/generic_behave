"""All common behave functions that are used in behave frameworks"""
# Ignoring prints in this file
# flake8: noqa
import logging
import re

import ansicolor
from behave.runner import Context
from requests import Session

# Initialize a logger
LOGGER = logging.getLogger(__name__)


class CommonBehave:
    """Class for all static common behave functions"""

    @staticmethod
    def interpolate_context_attributes(ctx: Context, value: str) -> str:
        """Function that will check the context to see if we have an attribute stored with that name.

        This function will parse out variable names with the following regex: {.*} taking all chars between braces
        If the string value read in is None at the start -> return None

        Args:
            ctx: behave context that holds our attribute and value
            value: the string to traverse for attributes on the context

        Returns:
            the new string with all context vars replaced with values

        """
        if value is None:
            return None
        else:
            # Parse and replace any dimension-measure names that use "." notation,
            # since Python would otherwise throw an error trying to receive properties for a
            # non-existent object during string interpolation
            parameters = re.findall(r"\{([.,\w-]+)\}", value)
            for parameter in parameters:
                if "." in parameter:
                    dm_id = ctx.dimensions_measures_map[parameter]
                    value = value.replace("{" + parameter + "}", dm_id)

            # Replace the rest with properties on the context
            namespace = {param: getattr(ctx, param) for param in parameters}
            return value.format(**namespace)

    @staticmethod
    def get_test_user_client(ctx: Context, user: str) -> Session:
        """Get a user session object form the test_users dict in the behave context

        Args:
            ctx: The behave context
            user: The user to get the session for

        Returns:
            The requests.Session object for the specific user

        """
        test_users = getattr(ctx, "test_users")
        if user in test_users:
            return test_users[user]["client"]
        else:
            raise Exception(
                f"The session for user: {user} was not found stored on the behave context."
            )

    @staticmethod
    def get_test_user_id(ctx: Context, user: str) -> str:
        """Get a user id from the test_users dict in the behave context

        Args:
            ctx: The behave context
            user: The user to get the ID for

        Returns:
            The ID for the specific user

        """
        test_users = getattr(ctx, "test_users")
        if user in test_users:
            return test_users[user]["user_id"]
        else:
            raise Exception(
                f"The ID for user: {user} was not found stored on the behave context."
            )

    @staticmethod
    def log_context_attributes(ctx: Context) -> None:
        """Get the context attributes stored on context

        Args:
            ctx: The behave context

        """
        LOGGER.debug("Current attributes saved to context:")
        if ctx.config.logging_level == 10:
            # For each layer of the context log the layer and make a table of attributes
            print("\n")
            for layer in ctx._stack:
                print(
                    ansicolor.blue(
                        "-------------------------------------------------------------------------"
                    )
                )
                print(ansicolor.blue(f"CONTEXT LAYER: {layer['@layer']}"))
                print(
                    ansicolor.blue(
                        "-------------------------------------------------------------------------"
                    )
                )
                # pretty print out each key value pair in a table
                for key in layer:
                    # Don't log standard attributes that are none
                    if layer[key] is not None:
                        print("%s %s| %r" % (key, " " * (30 - len(key)), layer[key]))
                print(
                    ansicolor.blue(
                        "-------------------------------------------------------------------------"
                    )
                )
            print("\n")
