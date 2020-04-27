"""Generic step definitions for REST APIs"""

import logging
from typing import Dict, Union
import uuid

from behave import given, step, use_step_matcher
from behave.runner import Context
from jsonpath import jsonpath
from ....ns_behave.common.common_behave_functions import CommonBehave

# Enable the regex step matcher for behave in this class
use_step_matcher("re")
# Set up a logger
LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------------
# Generic steps for headers
# ------------------------------------------------------------------------


@step('request header "(?P<header>.*)" is set to "(?P<header_value>.*)"')
def step_set_request_header(ctx: Context, header: str, header_value: str) -> None:
    """Sets a given type of request header to a given value.

    Args:
        ctx: The behave context
        header: The type of request header
        header_value: The value the request header should have

    """
    ctx.headers = {}
    desired_value = CommonBehave.interpolate_context_attributes(ctx, header_value)
    LOGGER.debug(f"Attempting to set request header: {header} to: {header_value}.")
    if desired_value.lower() in ("invalid", "empty", "empty string"):
        ctx.headers[header] = ""
    elif desired_value.lower() in ("none", "null"):
        ctx.headers[header] = None
    else:
        ctx.headers[header] = desired_value
    LOGGER.debug(
        f"Successfully set request header: {header} to: {ctx.headers[header]}."
    )


@given("request headers(?::|)?")
def step_set_request_headers(ctx: Context) -> None:
    """Sets a table of given request headers to given values.

    Args:
        ctx: The behave context

    """
    ctx.headers = {}
    for row in ctx.table:
        step_set_request_header(ctx, row[0], row[1])


# ------------------------------------------------------------------------
# Generic steps for context memory and variables
# ------------------------------------------------------------------------


@given('the value "(?P<value>.*)" is saved as "(?P<value_name>.*)"')
def step_save_variable_to_context(ctx: Context, value: str, value_name: str) -> None:
    """Sets a variable to an attribute of the behave context

    Args:
        ctx: The behave context
        value: The name the new attribute in the behave context should have
        value_name: The value of the new attribute in the behave context

    """
    setattr(ctx, value_name, value)
    LOGGER.debug(f"Successfully saved value: {value} as {value_name}.")


@step('the context value at "(?P<context_attribute>.*)" is printed')
def step_print_context_attribute_value(ctx: Context, context_attribute: str) -> None:
    """Prints the value of an attribute from the behave context to the debug logger

    Args:
        ctx: The behave context
        context_attribute: The attribute in the behave context that should be printed

    """
    found_value = getattr(ctx, context_attribute)
    if found_value:
        LOGGER.debug(
            f"Context attribute: key: '{context_attribute}' value: '{found_value}'"
        )
    else:
        raise AttributeError(
            f"No attribute '{context_attribute}'' found saved on the context"
        )


@step('the (?:JSON|json)? response at "(?P<key>.*)" is saved as "(?P<value_name>.*)"')
def step_save_response_attribute_to_context(
    ctx: Context, key: str, value_name: str
) -> None:
    """Sets the JSON response with a given key to a value in the behave context with an attribute name of <value_name>

    Args:
        ctx: The behave context
        key: The key from the JSON response
        value_name: The new name for the new attribute in the behave context

    """
    interpolated_key = CommonBehave.interpolate_context_attributes(ctx, f"$.{key}")
    list_of_values = jsonpath(ctx.response.json(), interpolated_key)
    LOGGER.debug(
        f"Attempting to save JSON response at: {interpolated_key} as: {value_name}."
    )
    if list_of_values:
        found_value = list_of_values[0]
        setattr(ctx, value_name, found_value)
        LOGGER.debug(f"Successfully saved response attribute: {key} as {value_name}.")
    else:
        raise KeyError(
            f"No key: '{interpolated_key}' found in the JSON response: {ctx.response.json()}"
        )


@step("the (?i)(?:JSON|json)? response is saved as the following(?::|)?")
def step_save_response_attributes_to_context(ctx: Context) -> None:
    """The key values in the first column are saved to context with the name under the second column.

    Args:
        ctx: The behave context

    """
    for row in ctx.table:
        step_save_response_attribute_to_context(ctx, row[0], row[1])


@given('the (?:JSON|json)? payload at "(?P<key>.*)" is saved as "(?P<value_name>.*)"')
def step_save_request_attribute_to_context(
    ctx: Context, key: str, value_name: str
) -> None:
    """Set a value from the request payload to the behave context

    Args:
        ctx: The behave context
        key: The key from the request payload to save
        value_name: The name the new attribute should have in the behave context

    """
    LOGGER.debug(f"Attempting to save JSON payload at: {key} as: {value_name}.")
    list_of_values = jsonpath(ctx.request_data, f"$.{key}")
    if list_of_values:
        found_value = list_of_values[0]
        setattr(ctx, value_name, found_value)
        LOGGER.debug(
            f"Successfully saved the JSON payload at: {value_name} as: {found_value}."
        )
    else:
        raise KeyError(
            f"No key: '{key}' found in the request_data saved on the context: {ctx.request_data}"
        )


@step(
    'the position where "(?P<key>.*)" is "(?P<value>.*)" is saved from the JSON response(?: at "(?P<json_key>.*)")?'
)
def step_save_position_attribute_to_context(
    ctx: Context, key: str, value: str, json_key: str = None
) -> None:
    """
    Attempts to obtain a key from the JSON response and set the value of that key to the behave context

    Args:
        ctx: The behave context
        key: The positional key that is being searched for
        value: The value the positional key should have
        json_key: The json key that indicates where the search for the positional key should occur

    """
    interpolated_key = CommonBehave.interpolate_context_attributes(ctx, key)
    interpolated_value = CommonBehave.interpolate_context_attributes(ctx, value)
    # Check if we are at the root of the json. If we are then use the '.' instead of the json key
    if json_key:
        list_of_values = jsonpath(ctx.response.json(), json_key)
    else:
        list_of_values = jsonpath(ctx.response.json(), ".")
    LOGGER.debug(
        f"Attempting to find position where key: {key} is value: {value} at: {list_of_values}."
    )
    if list_of_values:
        json_objects = list_of_values[0]
        for json_object in json_objects:
            if json_object[interpolated_key] == interpolated_value:
                setattr(ctx, "position", str(json_objects.index(json_object)))
                LOGGER.debug(
                    f"Successfully saved position as: {ctx.position} for key: {key} and value {value} at {list_of_values}."
                )
                break
        else:
            raise KeyError(
                f"No key: '{interpolated_key}' found in the dictionary: {json_object}"
            )
    else:
        raise KeyError(
            f"No collection found at '{json_key}' in the JSON response: {ctx.response.json()}"
        )


# ------------------------------------------------------------------------
# Generic steps for modifying JSON (dictionaries)
# ------------------------------------------------------------------------


@given(
    'the (?:JSON|json)? request payload at "(?P<target_key>.*)" is modified to be "(?P<value>.*)"'
)
def step_generic_modify_request_json(ctx: Context, target_key: str, value: str) -> None:
    """Modifies the request data in the behave context to have the actual value of the given string representation.

    Args:
        ctx: The behave context
        target_key: The key whose value is to be modified
        value: A string representation of what the new value should be

    """
    LOGGER.debug(
        f"Attempting to modify the JSON request payload at: {target_key} to be: {value}."
    )
    desired_value = CommonBehave.interpolate_context_attributes(ctx, value)
    parsed_key = CommonBehave.interpolate_context_attributes(ctx, target_key)
    if desired_value.lower() in ("none", "null"):
        ctx.request_data = modify_json_value(ctx.request_data, parsed_key, None)
    elif desired_value.lower() in ("invalid", "empty", "empty string"):
        ctx.request_data = modify_json_value(ctx.request_data, parsed_key, "")
    elif desired_value.lower() in "uuid":
        ctx.request_data = modify_json_value(
            ctx.request_data, parsed_key, str(uuid.uuid4())
        )
    else:
        ctx.request_data = modify_json_value(
            ctx.request_data, parsed_key, desired_value
        )
    LOGGER.debug("Successfully updated JSON request payload.")


# ------------------------------------------------------------------------
# Generic steps for creating JSON payloads (dictionaries)
# ------------------------------------------------------------------------


@given("request data from the previous request")
def step_set_previous_request_data(ctx: Context) -> None:
    """Sets the data from the previous request payload to the request data for the current request.

    Args:
        ctx: The behave context

    """
    LOGGER.debug(
        "Attempting to set the request data to the last used request_data value"
    )
    ctx.request_data = ctx.previous_payload
    LOGGER.debug(f"Successfully set the request data to: {ctx.request_data}")


@given('request data from context variable "(?P<context_variable>.*)"')
def step_set_request_data_from_ctx_var(ctx: Context, context_variable: str) -> None:
    """Reads a variable name without the {} and change to the value in context.

    It is then saved to the context as request_data.

    Args:
        ctx: The behave context
        context_variable: The context variable to search for via get_attr()

    """
    LOGGER.debug(
        f"Attempting to set the request_data on context from a context variable: {context_variable}"
    )
    ctx.request_data = getattr(ctx, context_variable)
    LOGGER.debug(f"ctx.request _data is set to: {ctx.request_data}\n\n")


@given(
    'the following (?:JSON|json)? payload(?::|)?(?: saved as "(?P<value_name>.*)"(?::|)?)?'
)
def step_generic_json_dictionary(ctx: Context, value_name: str = None) -> None:
    """Sets the given table representing a request payload to an attribute in the behave context as a given name.

    Args:
        ctx: The behave context
        value_name: The name of the attribute in the behave context

    """
    LOGGER.debug(f"Attempting to save payload as: {value_name}.")
    payload: Dict[str, Union[str, int]] = {}
    for row in ctx.table:
        value = CommonBehave.interpolate_context_attributes(ctx, row[1])
        # If value is a digit .. cast to int
        if value.isdigit():
            payload[row[0]] = int(value)
        else:
            payload[row[0]] = value
    # If value_name is specified, set a context attribute with that name equal to the payload.
    # Else set ctx.request_data equal to the payload.
    if value_name:
        setattr(ctx, value_name, payload)
    else:
        ctx.request_data = payload
    LOGGER.debug(f"Successfully saved payload: {payload} as: {value_name}.")


# ------------------------------------------------------------------------
# Supporting functions for steps
# ------------------------------------------------------------------------


def modify_json_value(
    current_payload: dict, path_to_value: str, new_value: str
) -> dict:
    """Function that will recursively traverse a dictionary and replace a value at a given key.

    The "key" is evaluated using JSON path such as "first_key.nested_key" when we have nested dictionaries.

    Args:
        current_payload: the dictionary we want to recursively search for a key value pair to replace
        path_to_value: the JSON path expression of the key to search for
        new_value: The new value we will replace at the key once found

    """
    if "." not in path_to_value:
        current_payload[path_to_value] = new_value
        return current_payload
    else:
        first_key = path_to_value.split(".")[0]
        remaining_keys = ".".join(path_to_value.split(".")[1:])
        # TODO: QUALITY-713 - evaluate 'first_key' and check if it contains []. If so we need to traverse in the array.
        if first_key in current_payload:
            current_payload[first_key] = modify_json_value(
                current_payload[first_key], remaining_keys, new_value
            )
        else:
            raise KeyError(
                f"No key: '{first_key}' found in the request payload: {current_payload}"
            )
        return current_payload
