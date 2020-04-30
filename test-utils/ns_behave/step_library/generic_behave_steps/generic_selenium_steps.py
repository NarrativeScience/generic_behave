"""
Generic selenium steps that will allow for all generic selenium actions. Some examples of this:
1) Setting the page size in pixels
2) Navigating to a custom URL
3) Verifying page URL
4) Verifying page title
"""
import logging

from behave import given, step, then, use_step_matcher, when
from behave.runner import Context
from ns_selenium.selenium_functions.assert_functions import AssertFunctions
from ns_selenium.selenium_functions.click_functions import ClickFunctions
from ns_selenium.selenium_functions.general_functions import GeneralFunctions
from ns_selenium.selenium_functions.input_functions import InputFunctions
from ns_selenium.selenium_functions.wait_functions import WaitFunctions

# Initialize a logger

LOGGER = logging.getLogger(__name__)

# Enable the regex step matcher for behave in this class
use_step_matcher("re")


@when("the user navigates to (?P<endpoint>.*)")
def step_url_navigation(ctx: Context, endpoint: str) -> None:
    """
    Navigate to a page by it's url

    Args:
        ctx: The behave context
        endpoint: The url of the page without the base host name

    """
    LOGGER.debug(f"Attempting to navigate to {ctx.host}{endpoint}")
    ctx.driver.get(f"{ctx.host}{endpoint}")
    LOGGER.debug(f"Successfully navigated to {ctx.host}{endpoint}")


@when("the (?P<link>.[_\w\s]+) is clicked")
def step_link_clicked(ctx: Context, link: str) -> None:
    """Click a link on a particular page

    Args:
        ctx: The Behave context
        link: The link that should be clicked

    """
    link = sanitize(link)
    WaitFunctions.wait_for_element_to_be_clickable(ctx, ctx.locators, link)
    ClickFunctions.click_element_by_name(ctx, ctx.locators, link)


@when("the following links are clicked(?::|)")
def step_links_clicked_in_order(ctx: Context) -> None:
    """Click a series of links in order

    Args:
         ctx: The behave context

    """
    for row in ctx.table:
        step_link_clicked(ctx, row[0])


@then(
    "the (?P<element>[_\w\s]+) element should (?P<should_not_be_present>|not )be present(?: after (?P<timeout>\d+) seconds)?"
)
def step_assert_element_is_present(
    ctx: Context, element: str, should_not_be_present: str = None, timeout: str = None
) -> None:
    """Assert that the provided dropdown option is present

    Args:
        ctx: The behave context
        element: The element expected to be present
        should_not_be_present: String to determine if the element should or should not be present
        timeout: The amount of time to wait for the element to be present or absent

    """
    element = sanitize(element)
    arguments_tuple = (ctx, ctx.locators, element, int(timeout)) if timeout else (ctx, ctx.locators, element)
    WaitFunctions.wait_until_element_not_present(
        *arguments_tuple
    ) if should_not_be_present else WaitFunctions.wait_for_presence_of_element(
        *arguments_tuple
    )
    assert (
        AssertFunctions.element_is_not_present(*arguments_tuple)
        if should_not_be_present
        else AssertFunctions.element_is_present(*arguments_tuple)
    )


@then(
    "(?P<multiple_exist>one of )?the (?P<element>[_\w\s]+) element(?:s)? should have text (?P<expected_text>[-_\w\s]+)"
)
def step_assert_element_text(
    ctx: Context, multiple_exist: str, element: str, expected_text: str
) -> None:
    """Assert that the provided dropdown option is present

    Args:
        ctx: The behave context
        multiple_exist: A string
        element: The element expected to be present
        expected_text: The text the element is expected to have

    """
    sanitized_element = sanitize(element)
    arguments_tuple = (ctx, ctx.locators, sanitized_element)
    if multiple_exist:
        actual_text = " ".join(
            GeneralFunctions.get_elements_text_by_name(*arguments_tuple)
        )
    else:
        actual_text = GeneralFunctions.get_elements_text_by_name(*arguments_tuple)
    assert (
        expected_text in actual_text
    ), f"Expected the {element} element to have text: {expected_text} by its text was {actual_text}"


@then("the (?P<element>[_\w]+) element should have the following text(?::|)?")
def step_assert_element_text_multiline(ctx: Context, element: str) -> None:
    """Assert that the provided dropdown option is present

    Args:
        ctx: The behave context
        element: The element expected to be present

    """
    for row in ctx.table:
        step_assert_element_text(ctx, "", element, row[0])


@then("the following elements should be present(?::|)?")
def step_assert_elements_are_present(ctx: Context) -> None:
    """Assert that the provided dropdown options are present

    Args:
        ctx: The behave context

    """
    for row in ctx.table:
        step_assert_element_is_present(ctx, row[0])


@then("the (?P<page>[_\w]+) page should be open(?: after (?P<timeout>\d+) seconds)?")
def step_assert_page_open(ctx: Context, page: str, timeout: str) -> None:
    """Assert that a given page is open

    Args:
        ctx: The behave context
        page: The page that should be open
        timeout: (Optional) The amount of time to wait for the page to be open

    """
    arguments_tuple = (ctx, ctx.locators, f"{page.lower()}_page_locator")
    if timeout is not None:
        WaitFunctions.wait_for_element_to_be_clickable(*arguments_tuple, float(timeout))
    WaitFunctions.wait_for_element_to_be_clickable(*arguments_tuple)
    ClickFunctions.click_element_by_name(*arguments_tuple)
    AssertFunctions.validate_page_url(ctx, ctx.page_name_dict, page)


@then("the url should contain (?P<text>[-_\w\d]+)")
def step_asset_url_contains(ctx: Context, text: str) -> None:
    """Assert that the url contains given text

    Args:
        ctx: The behave context
        text: The text that is expected to be in the url

    """
    assert AssertFunctions.validate_url_contains(
        ctx, text
    ), f"Expected the url to contain {text} but it did not"


@step("(?P<text>[-._\w\d\s]+) is input into (?P<text_box>[_\w\s]+)")
def step_input_data(ctx: Context, text: str, text_box: str) -> None:
    """

    Args:
        ctx: The behave context.
        text: The text to put into the text box
        text_box: The box that will contain the input text

    """
    sanitized_text_box = sanitize(text_box)
    LOGGER.debug(f"Attempting to fill the {text_box} with {text}")
    arguments_tuple = (ctx, ctx.locators, sanitized_text_box)
    WaitFunctions.wait_for_visibility_of_element(*arguments_tuple)
    InputFunctions.send_keys_to_element_by_name(*arguments_tuple, text)
    LOGGER.debug(f"Successfully filled the {text_box} with {text}")


@step("(?P<text_box>[_\w\s]+)(?: (?P<text_box_index>\d+))? is cleared?")
def step_text_box_cleared(ctx: Context, text_box: str, text_box_index: str) -> None:
    """
    Clear the text from the given text box

    Args:
        ctx: The behave context
        text_box: The text box whose input should be reset
        text_box_index: (Optional) Which of the matched elements should be selected

    """
    LOGGER.debug(f"Attempting to clear the {text_box} {text_box_index}")
    sanitized_text_box = sanitize(text_box)
    arguments_tuple = (ctx, ctx.locators, sanitized_text_box)
    WaitFunctions.wait_for_element_to_be_clickable(*arguments_tuple)
    if text_box_index is None:
        InputFunctions.clear_text_by_element_name(*arguments_tuple)
    else:
        InputFunctions.clear_text_by_index_in_list_of_elements(
            *arguments_tuple, int(text_box_index)
        )
    LOGGER.debug(f"Successfully cleared the {text_box} {text_box_index}")


@given("the browser size of (?P<width>\d+)x(?P<height>\d+)")
def step_set_browser_size(ctx: Context, width: int, height: int) -> None:
    """
    This step will set the browser size to a custom dimension for width and height.
    Args:
        ctx: The behave context.
        width: The width to set.
        height: The height to set.
    """
    LOGGER.debug(f"Attempting to set the browser size to {width}x{height}")
    ctx.driver.set_wigndow_size(width, height)
    LOGGER.debug(f"Browser size successfully set to {width}x{height}")


@given("the (?P<checkbox>[_\w\d\s]+) checkbox is (?P<check_status>unchecked|checked)")
def step_ensure_box_is_checked_or_not_checked(
    ctx: Context, checkbox: str, check_status: str
) -> None:
    """Ensure that a checkbox is checked or unchecked.

    Args:
        ctx: The behave context
        checkbox: The checkbox element to be checked or unchecked
        check_status: Whether or not the checkbox should be checked

    """
    LOGGER.debug(f"Attempting to ensure that the {checkbox} is {check_status}.")
    sanitized_checkbox = sanitize(checkbox)
    arguments_tuple = (ctx, ctx.locators, sanitized_checkbox)
    class_name = GeneralFunctions.get_element_by_name(*arguments_tuple).get_attribute(
        "class"
    )
    if (
        "checked" in class_name
        and check_status == "unchecked"
        or "checked" not in class_name
        and check_status == "checked"
    ):
        WaitFunctions.wait_for_element_to_be_clickable(*arguments_tuple)
        ClickFunctions.click_element_by_name(*arguments_tuple)
    LOGGER.debug(f"Successfully ensured that the {checkbox} is {check_status}.")


@then(
    "the (?P<checkbox>[_\w\s\d]+) checkbox should be (?P<check_status>unchecked|checked)"
)
def step_assert_box_is_checked_or_not_checked(
    ctx: Context, checkbox: str, check_status: str
) -> None:
    """Assert that a checkbox is checked or unchecked.

    Args:
        ctx: The behave context
        checkbox: The checkbox element to be checked or unchecked
        check_status: Whether or not the checkbox should be checked

    """
    LOGGER.debug(f"Attempting to assert that the {checkbox} is {check_status}.")
    sanitized_checkbox = sanitize(checkbox)
    arguments_tuple = (ctx, f"{sanitized_checkbox}_enabled")
    WaitFunctions.wait_for_visibility_of_element(ctx, ctx.locators, sanitized_checkbox)
    assert (
        AssertFunctions.element_is_not_present(*arguments_tuple)
        if check_status == "checked"
        else AssertFunctions.element_is_present(*arguments_tuple)
    ), f"The {checkbox} was supposed to be {check_status} but it was not."
    LOGGER.debug(f"Successfully asserted that the {checkbox} is {check_status}.")


@then("the (?P<button>[-_\w]+) should be (?P<status>disabled|enabled)")
def step_assert_button_is_disabled(ctx: Context, button: str, status: str):
    """Assert that a button is enabled or disabled

    Args:
        ctx: The behave context
        button: The name of the locator corresponding to the button
        status: String to determine whether the button should be enabled or disabled

    """
    LOGGER.debug(f"Attempting to assert that the {button} is {status}.")
    assert AssertFunctions.element_is_active(
        ctx, ctx.locators, button
    ), f"The {button} was supposed to be {status} but it was not."
    LOGGER.debug(f"Successfully asserted that the {button} is {status}.")


@step("the alert is confirmed")
def step_confirm_alert(ctx: Context) -> None:
    """Wait for the alert to be clickable and click it

    Args:
        ctx: The behave context
    """
    WaitFunctions.wait_for_presence_of_alert(ctx)
    GeneralFunctions.confirm_alert(ctx)


@then(
    "the (?P<element>[-\w\d\s]+) should be present (?P<quantity>\d+) (?P<relative_quantity>|more )?time(?:s)?"
)
def step_assert_element_quantity(
    ctx: Context, element: str, quantity: str, relative_quantity: str
) -> None:
    """Checks how many of the given element appear on the page

    Args:
        ctx: Context
        element: The element to find
        quantity: The number of the given element that should be present
        relative_quantity: A string to determine if the given quantity is relative to the previous quantity
            (see step_determine_element_quantity()) or an absolute quantity

    """
    sanitized_element = sanitize(element)
    expected_quantity = (
        int(quantity) + ctx.quantities[sanitized_element]
        if relative_quantity
        else int(quantity)
    )
    if quantity == 0:
        step_assert_element_is_present(ctx, element, "not")
        return
    actual_quantity = len(GeneralFunctions.get_elements_by_name(ctx, ctx.locators, sanitized_element))
    assert (
        actual_quantity == expected_quantity
    ), f"Expected there to be {expected_quantity} of {element} but there were {actual_quantity} elements."


@given("the (?P<element>[-\w\d\s]+)'s quantity is saved")
def step_determine_element_quantity(ctx: Context, element: str) -> None:
    """Checks how many of the given element appear on the page

    Args:
        ctx: Context
        element: The element to find

    """
    ctx.quantities = {} if not hasattr(ctx, "quantities") else ctx.quantities
    sanitized_element = sanitize(element)
    ctx.quantities[sanitized_element] = len(
        GeneralFunctions.get_elements_by_name(ctx, ctx.locators, sanitized_element)
    )


@given(
    "the (?P<element>[-\w\d\s]+) is present no more than (?P<quantity>\d+) time(?:s)?"
)
def step_remove_additional_elements(ctx: Context, element: str, quantity: str) -> None:
    """
    Cleanup function used to remove extraneous elements from a page.
        Clicking on an element must remove the element in order for
        this step to work.

    Args:
        ctx: The behave context
        element: The element to be clicked and removed
        quantity: The times the element should appear on the page

    """
    sanitized_element = sanitize(element)
    expected_quantity = int(quantity)
    count = len(GeneralFunctions.get_elements_by_name(ctx, ctx.locators, sanitized_element))
    while count > expected_quantity:
        ClickFunctions.click_element_by_name(ctx, ctx.locators, sanitized_element)
        count -= 1


def sanitize(string: str) -> str:
    """Function used to clean strings in order to provide a standard input for other functions

    Args:
        string: The string to be sanitized

    """
    return string.lower().replace(" ", "_").strip()
