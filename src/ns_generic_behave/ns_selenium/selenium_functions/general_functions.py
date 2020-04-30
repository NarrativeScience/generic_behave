import logging
from typing import List, Union

from behave.runner import Context
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGGER = logging.getLogger(__name__)


class GeneralFunctions:
    """
    All selenium element general functions
    """

    @staticmethod
    def get_element_by_name(
        ctx: Context, locators: dict, element_name: str
    ) -> WebElement:
        """Find an element using the locator from its page object.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator strategy
                in the page object's locators dictionary.

        Returns:
            The WebElement found using the locator strategy for the given
                element key.

        Raises:
            :py:class:`.TimeoutException`: when the element can't be found
                using the given locator strategy.

        """
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Waiting for the presence of element: {element_name} with locator: {locator}."
            )
            # This log line is for behave spacing so the above debug message can be shown instead of overwritten
            LOGGER.debug("")
            element = WebDriverWait(ctx.driver, ctx.wait_timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f"Failed to find '{element_name}'."
                f"Waited {ctx.wait_timeout} seconds for {locator[0]} "
                f"{locator[1]}, but never found it. That's a bummer, but stay "
                f"positive!"
            )
        return element

    @staticmethod
    def get_elements_by_name(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> List[WebElement]:
        """Find a group of elements using their locator from their page object.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the locator strategy for the
                group of elements in the page object's locators dictionary.
            timeout: seconds to wait for the element to appear or None.
            Default is set in the environment.py file

        Returns:
            A list of WebElements found using the locator strategy for the
                given element key.

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(f"Waiting for the presence of element: {element_name}.")
            elements = WebDriverWait(ctx.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f"Failed to find '{element_name}'."
                f"Waited {ctx.wait_timeout} seconds for {locator[0]} "
                f"{locator[1]}, but never found it. That's a bummer, but stay "
                f"positive!"
            )
        return elements

    @staticmethod
    def get_elements_text_by_name(
        ctx: Context, locators: dict, element_name: str
    ) -> str:
        """Find a elements text using their locator from their page object.

        Args:
            ctx: The behave context object
            locators: dict of element locators
            element_name: key corresponding to the locator strategy for the
                group of elements in the page object's locators dictionary

        Returns:
            A string value of the text at that element

        """
        LOGGER.debug(f"Attempting to get text for {element_name}")
        element_text = GeneralFunctions.get_element_by_name(
            ctx, locators, element_name
        ).text
        LOGGER.debug(f"Found text: '{element_text}' at '{element_name}'")
        return element_text

    @staticmethod
    def scroll_to_element(ctx: Context, element: WebElement) -> None:
        """Scroll the page untill the element is in the center.

        Args:
            ctx: The behave context object
            element: element to scroll to

        """
        LOGGER.debug("Scrolling to the element")
        ctx.driver.execute_script(
            "return arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });",
            element,
        )

    @staticmethod
    def move_to_element(ctx: Context, element: WebElement) -> None:
        """Move the page to an element if it is not visible.

        Args:
            ctx: The behave context object
            element: element to move to

        """
        LOGGER.debug("Moving to element")
        ActionChains(ctx.driver).move_to_element(element).perform()

    @staticmethod
    def switch_to_active_window(ctx: Context, handle_num: int) -> None:
        """Switches to the active window after a new tab is opened"""
        LOGGER.debug("Switching to active window.")
        ctx.driver.switch_to.window(ctx.driver.window_handles[handle_num])

    @staticmethod
    def close_active_window(ctx: Context) -> None:
        """Closes the active window"""
        LOGGER.debug("Closing active window.")
        ctx.driver.close()

    @staticmethod
    def hover_over(ctx: Context, element: WebElement) -> None:
        """Hover mouse over an element

        Args:
            ctx: The behave context object
            element: WebElement to hover over

        """
        LOGGER.debug(f"Hovering over element.")
        ActionChains(ctx.driver).move_to_element(element).perform()

    @staticmethod
    def set_cache_item(ctx: Context, key: str, value: str) -> None:
        """set localStorage cache key to a value

        Args:
            ctx: The behave context object
            key: cache key to be set
            value: value to set key to

        """
        LOGGER.debug(f"Setting local storage cache: ('{key}', '{value}')")
        ctx.driver.execute_script(f"window.localStorage.setItem('{key}', {value})")

    @staticmethod
    def update_locator(
        ctx: Context,
        locators: dict,
        locator: str,
        surrounding_text: tuple,
        replacement_name: str,
    ) -> None:
        """
        Update a locator in the locators dict by replacing a static value with a dynamic one

        Args:
            ctx: The behave context
            locators: Dict of locators
            locator: The particular locator to be updated with a dynamic value
            surrounding_text:  A tuple where the first element is what comes before the dynamic value and the second
                element is what comes after the dynamic value
            replacement_name: The dynamic string value to replace the static stand in value

        """
        replacement_name = GeneralFunctions.sanitize_name(ctx, replacement_name)
        LOGGER.debug(
            f"Attempting to update the locator {locator} to a new dynamically generated value."
        )
        locator_tuple = (
            locators[locator][0],
            surrounding_text[0] + replacement_name + surrounding_text[1],
        )
        locators.update({locator: locator_tuple})
        LOGGER.debug(
            f"Successfully inserted the text {replacement_name} into the locator {locator}"
        )

    @staticmethod
    def sanitize_name(ctx: Context, name_to_sanitize: str) -> str:
        """
        Change variable name to one that has no whitespace and only contains lowercase letters

        Args:
            ctx: The behave context
            name_to_sanitize: The variable to be refactored
        """

        LOGGER.debug(
            f"Attempting to remove whitespace and lowercase all letters in {name_to_sanitize}"
        )
        return name_to_sanitize.strip().replace(" ", "-").lower()

    @staticmethod
    def get_element_status(ctx: Context, locators: dict, element_name: str) -> str:
        """Find a elements status using their locator from their page object.

        Args:
            ctx: The behave context object
            locators: dict of element locators.
            element_name: key corresponding to the locator strategy for the
                group of elements in the page object's locators dictionary

        Returns:
            A string value of the text at that element

        """
        LOGGER.debug(f"Attempting to get the status of {element_name}")
        element_status = GeneralFunctions.get_element_by_name(
            ctx, locators, element_name
        ).get_attribute("disabled")
        LOGGER.debug(f"The element {element_name} has a status of {element_status}")
        return element_status

    @staticmethod
    def confirm_alert(ctx: Context) -> None:
        """Confirm an alert using selenium

        Args:
            ctx: The behave context

        """
        ctx.driver.switch_to.alert.accept()
