"""Generic assertion step definitions for REST APIs"""

import logging

from behave import then, use_step_matcher
from behave.runner import Context
from jsonpath import jsonpath
from test_utils.behave.src.ns_behave.common.common_behave_functions import CommonBehave

# Enable the regex step matcher for behave in this class
use_step_matcher("re")
# Set up a logger
LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------------
# Generic steps for status codes
# ------------------------------------------------------------------------


@then("a (?P<status>[0-9]{3}) response is returned")
def step_assert_status_code(ctx: Context, status: int) -> None:
    """Checks if the response has the correct status code being returned.

    Args:
        ctx: The behave context
        status: The expected status code

    """
    LOGGER.debug(
        f"Status code expected: {status}. Status code returned: {ctx.response.status_code}"
    )
    assert ctx.response.status_code == int(
        status
    ), f"Status code expected: {status}. Status code returned: {ctx.response.status_code}"


# ------------------------------------------------------------------------
# Generic steps for headers
# ------------------------------------------------------------------------


@then(
    "the response content header should (?P<negate>not )?be (?P<header_type>JSON|HTML)"
)
def step_assert_content_header(ctx: Context, negate: str, header_type: str) -> None:
    """Checks if the response is json using it's content header.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        header_type: The type of expected response header (json or html)

    """
    expected_headers = {
        "JSON": "application/json; charset=utf-8",
        "HTML": "text/html; charset=utf-8",
    }
    header = ctx.response.headers.get("content-type")
    if negate:
        LOGGER.debug("Checking that the response content is not JSON.")
        assert (
            header != expected_headers[header_type]
        ), f'Expected response content-type header to not be "application/json", but it was "{header}"'
        LOGGER.debug("Validated that the response content was not JSON.")
    else:
        LOGGER.debug("Checking that the response content is JSON.")
        assert (
            header == expected_headers[header_type]
        ), f'Expected response content-type header to be "application/json", but it was "{header}"'
        LOGGER.debug("Validated that the response content was JSON.")


@then("the response headers should (?P<negate>not )?be the following(?::|)?")
def step_assert_headers(ctx: Context, negate: str) -> None:
    """Checks that the headers have the proper values.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        header = ctx.response.headers.get(row[0])
        header_value = CommonBehave.interpolate_context_attributes(ctx, row[1])
        if negate:
            LOGGER.debug(
                f"Checking that the response header: {row[0]} should not be: {header_value}."
            )
            assert (
                header != header_value
            ), f'Expected response header: "{row[0]}" to not be "{header_value}", but it was "{header}"'
        else:
            LOGGER.debug(
                f"Checking that the response header: {row[0]} should be: {header_value}."
            )
            assert (
                header == header_value
            ), f'Expected response header: "{row[0]}" to be "{header_value}", but it was "{header}"'
        LOGGER.debug("Successfully validated response headers.")


# ------------------------------------------------------------------------
# Generic steps for REST responses
# ------------------------------------------------------------------------


@then("the (?:JSON|json)? response should have (?P<negate>no )?content")
def step_assert_rest_response_content(ctx: Context, negate: str) -> None:
    """Checks if the JSON response has content.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'no'. Otherwise, it will be None

    """
    if negate:
        LOGGER.debug("Checking that the JSON response should have no content.")
        assert (
            ctx.response.text is None or ctx.response.text == ""
        ), f"Expected no content in the response but found: {ctx.response.text}"
        LOGGER.debug(f"Successfully validated that the response had no content.")
    else:
        LOGGER.debug("Checking that the JSON response should have content.")
        assert (
            type(ctx.response.text) is str and len(ctx.response.text) > 0
        ), "Expected response to contain a payload but found none."
        LOGGER.debug(f"Successfully validated that the response had content.")


@then('the (?:JSON|json)? response should (?P<negate>not )?include "(?P<key>.*)"')
def step_assert_rest_response_key(ctx: Context, negate: str, key: str) -> None:
    """Checks that the JSON response contains a given key.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        key: The key that should be present in the response

    """
    list_of_values = jsonpath(
        ctx.response.json(),
        CommonBehave.interpolate_context_attributes(ctx, f"$.{key}"),
    )
    if negate:
        LOGGER.debug(f"Checking that the JSON response should not include key: {key}.")
        assert (
            not list_of_values
        ), f"Expected no key to be found at '{key}', but it was present. Response: {ctx.response.text}"
        LOGGER.debug(f"Validated that the JSON response did not include key: {key}.")
    else:
        LOGGER.debug(f"Checking that the JSON response should include key: {key}.")
        assert (
            list_of_values
        ), f"Expected key to be found at '{key}', but it was not present. Response: {ctx.response.text}"
        LOGGER.debug(f"Validated that the JSON response did include key: {key}.")


@then(
    "the (?:JSON|json)? response should (?P<negate>not )?include the following(?::|)?"
)
def step_assert_rest_response_key_table(ctx: Context, negate: str) -> None:
    """Checks that the JSON response contains all keys from a given table.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_rest_response_key(ctx, negate, row[0])


@then(
    'the (?:JSON|json)? response at "(?P<key>.*)" should (?P<negate>not )?have data type (?P<data_type>.*)'
)
def step_assert_rest_response_data_type(
    ctx: Context, key: str, negate: str, data_type: str
) -> None:
    """Checks that the key in the response is of the given data type.

    Args:
        ctx: The behave context
        key: The key in the response
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        data_type: The data type of the key

    """
    list_of_values = jsonpath(
        ctx.response.json(),
        CommonBehave.interpolate_context_attributes(ctx, f"$.{key}"),
    )
    if list_of_values:
        found_value = list_of_values[0]
        class_name = found_value.__class__.__name__
        if negate:
            LOGGER.debug(
                f"Checking that the JSON response at key: {key} should not have data type: {data_type}."
            )
            assert (
                class_name != data_type
            ), f"Expected the data type at key: '{key}' to not be '{data_type}', but we found: '{class_name}'"
            LOGGER.debug(
                f"Validated that the JSON response at key: {key} did not have data type: {data_type}."
            )
        else:
            LOGGER.debug(
                f"Checking that the JSON response at key: {key} should have data type: {data_type}."
            )
            assert (
                class_name == data_type
            ), f"Expected the data type at key: '{key}' to be '{data_type}', but we found: '{class_name}'"
            LOGGER.debug(
                f"Validated that the JSON response at key: {key} did have data type: {data_type}."
            )
    else:
        raise KeyError(
            f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
        )


@then(
    "the (?:JSON|json)? response should (?P<negate>not )?have the following data types(?::|)?"
)
def step_assert_rest_response_data_type_table(ctx: Context, negate: str) -> None:
    """Checks that the JSON response has keys of the given data types.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_rest_response_data_type(ctx, row[0], negate, row[1])


@then(
    'the (?:JSON|json)? response at "(?P<key>.*)" should (?P<negate>not )?be "(?P<value>.*)"'
)
def step_assert_rest_response_value(
    ctx: Context, key: str, negate: str, value: str
) -> None:
    """Generic step definition that will read in a key using json path and traverse the json to find the value.

    Assertions are done based on the negate flag.
    Json path is a language that allows you to find values in json based on an expression.
    Find more info on json path here: https://restfulapi.net/json-jsonpath/.

    Args:
        ctx: behave context
        negate: type of assert. Either should be or should not be. represented by optional gherkin syntax = 'no'
        key: json path key expression
        value: the expected value in the assert

    """
    list_of_values = jsonpath(
        ctx.response.json(), CommonBehave.interpolate_context_attributes(ctx, key)
    )
    desired_value = CommonBehave.interpolate_context_attributes(ctx, value)
    if list_of_values:
        found_value = str(list_of_values[0])

        if negate:
            LOGGER.debug(
                f"Checking that the JSON response at key: {key} should not be: {value}."
            )
            assert (
                found_value != desired_value
            ), f"Expected the JSON value at key: {key} to not be: {desired_value}, but we found: {found_value}"
            LOGGER.debug(
                f"Validated that the JSON response at key: {key} was not value: {value}"
            )
        else:
            LOGGER.debug(
                f"Checking that the JSON response at key: {key} should be: {value}."
            )
            assert (
                found_value == desired_value
            ), f"Expected the JSON value at key: {key} to be: {desired_value}, but we found: {found_value}"
            LOGGER.debug(
                f"Validated that the JSON response at key: {key} was value: {value}"
            )
    else:
        raise KeyError(
            f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
        )


@then("the (?:JSON|json)? response should (?P<negate>not )?be the following(?::|)?")
def step_assert_rest_response_value_table(ctx: Context, negate: str) -> None:
    """Checks that the JSON response have the given values.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None

    """
    for row in ctx.table:
        step_assert_rest_response_value(ctx, row[0], negate, row[1])


@then(
    'the (?:JSON|json)? response(?: at "(?P<key>.*)")? should (?P<negate>not )?have (?P<collection_size>[0-9]+) (?:.*)'
)
def step_assert_rest_response_collection_size(
    ctx: Context, key: str, negate: str, collection_size: str
) -> None:
    """Checks that the JSON response does or does not have a collection of the given size.

    Args:
        ctx: The behave context
        negate: A string representing whether or not a response should be negated. If it should be negated, it will have
            a value 'not'. Otherwise, it will be None
        key: The key in the JSON response where the collection size should be checked
        collection_size: The expected size of the collection

    """

    if key:
        list_of_values = jsonpath(
            ctx.response.json(), CommonBehave.interpolate_context_attributes(ctx, key)
        )
        if list_of_values:
            found_value = list_of_values[0]
            if isinstance(found_value, (dict, list)):
                if negate:
                    LOGGER.debug(
                        f"Checking that the JSON response at key: {key} should not have size: {collection_size}."
                    )
                    assert len(found_value) != int(collection_size), (
                        f"Expected the JSON value at key: {key} to not be a collection with size: {int(collection_size)},"
                        f" but we found: {len(found_value)} in the collection"
                    )
                    LOGGER.debug(
                        f"Validated that the JSON response at key: {key} did not have size: {collection_size}."
                    )
                else:
                    LOGGER.debug(
                        f"Checking that the JSON response at key: {key} should have size: {collection_size}."
                    )
                    assert len(found_value) == int(collection_size), (
                        f"Expected the JSON value at key: {key} to be a collection with size: {int(collection_size)},"
                        f" but we found: {len(found_value)} in the collection"
                    )
                    LOGGER.debug(
                        f"Validated that the JSON response at key: {key} did have size: {collection_size}."
                    )
            else:
                raise TypeError(
                    f"No dict or list found at key: '{key}'. We found: {type(found_value).__name__}"
                )
        else:
            raise KeyError(
                f"No key: '{key}' found in the JSON response: {ctx.response.json()}"
            )
    else:
        LOGGER.debug(
            f"Checking that the JSON response should have size: {collection_size}."
        )
        found_value = len(ctx.response.json())
        assert found_value == int(collection_size), (
            f"Expected the JSON value to be a collection with size: {int(collection_size)},"
            f" but we found: {found_value} in the collection"
        )
        LOGGER.debug(
            f"Validated that the JSON response did have size: {collection_size}."
        )
