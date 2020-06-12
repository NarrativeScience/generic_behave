import logging
import time
from typing import Union

from behave.runner import Context
from ns_selenium.utils.custom_webdriver_conditions import (
    element_is_of_length,
    element_not_present,
    text_to_change,
)
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Create a logger instance
LOGGER = logging.getLogger(__name__)


class WaitFunctions:
    """
    All selenium wait functions
    """

    @staticmethod
    def wait_for_presence_of_element(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> bool:
        """Wait until the specified element is present on the page.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator in the
                page object's locators dictionary.
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was not present after the timeout
                was reached

        Returns:
            True if element is present
        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(f"Waiting for the presence of element: {element_name}")
            WebDriverWait(ctx.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            LOGGER.debug(f"Element: {element_name} was found to be present")
            return True
        except TimeoutException:
            raise TimeoutException(
                f"The '{element_name}' element was not present when it"
                " was expected to be on the page."
            )

    @staticmethod
    def wait_for_presence_of_frame_then_switch(
        ctx: Context,
        frame_name: str,
        timeout: Union[int, None] = None,
    ) -> bool:
        """Wait until the specified frame is present on the page and switch to it.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator in the
                page object's locators dictionary.
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was not present after the timeout
                was reached

        Returns:
            True if element is present
        """
        timeout = timeout or ctx.wait_timeout
        try:
            LOGGER.debug(f"Waiting for the presence of frame: {frame_name}")
            WebDriverWait(ctx.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(frame_name)
            )
            LOGGER.debug(f"Frame: {frame_name} was found to be present and was switched to.")
            return True
        except TimeoutException:
            raise TimeoutException(
                f"The '{frame_name}' frame was not present when it"
                " was expected to be on the page."
            )

    @staticmethod
    def wait_until_element_not_present(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> None:
        """Wait until the specified element is not present on the page

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator strategy
                in the page object's locators dictionary.
            timeout: seconds to wait for the element to disappear or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was still present after the
                timeout was reached

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Waiting for element: {element_name} to no longer be present."
            )
            WebDriverWait(ctx.driver, timeout).until(element_not_present(locator))
        except TimeoutException:
            raise TimeoutException(
                f"The '{element_name}' element was "
                "present when it was not expected to be. Way to crash"
                f" the party, {element_name}."
            )

    @staticmethod
    def wait_until_element_is_of_length(
        ctx: Context,
        locators: dict,
        element_name: str,
        expected_length: int,
        timeout: Union[int, None] = None,
    ) -> None:
        """Wait until the specified element has the specified length

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator strategy
                in the page object's locators dictionary.
            expected_length: the desired length for the element
            timeout: seconds to wait for the element to disappear or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was not of the expected length
                after the time limit was reached

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Waiting for element: {element_name} to be of length: {expected_length}."
            )
            WebDriverWait(ctx.driver, timeout).until(
                element_is_of_length(locator, expected_length)
            )
        except TimeoutException:
            raise TimeoutException(
                f"The '{element_name}' element was not"
                f" of length {expected_length} when it was supposed to be. Way"
                f" to crash the party, {element_name}."
            )

    @staticmethod
    def wait_until_new_window_is_open(
            ctx: Context,
            expected_window_count: int,
            timeout: Union[int, None] = None,
    ) -> bool:
        """Wait until the expected amount of windows are open.

        Args:
            ctx: The behave context object.
            expected_window_count: The amount of windows expected to be open.
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was not present after the timeout
                was reached

        Returns:
            True if element is present
        """
        timeout = timeout or ctx.wait_timeout
        try:
            LOGGER.debug(f"Waiting for {expected_window_count} windows to be open")
            WebDriverWait(ctx.driver, timeout).until(
                EC.number_of_windows_to_be(expected_window_count)
            )
            LOGGER.debug(f"Successfully detected {expected_window_count} windows are open.")
            return True
        except TimeoutException:
            raise TimeoutException(
                f"Only {len(ctx.driver.window_handles)} window(s) were found open."
                f" Expected to be {expected_window_count} windows."
            )

    @staticmethod
    def wait_for_visibility_of_element(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> None:
        """Wait until the specified element is visible on the page.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator in the
                page object's locators dictionary.
            timeout: seconds to wait for the element to be visible or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was not visible after the timeout
                was reached

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Waiting for element: {element_name} to be visible on the page."
            )
            WebDriverWait(ctx.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f"The '{element_name}' element was not visible when it"
                " was expected to be on the page."
            )

    @staticmethod
    def wait_for_element_to_be_clickable(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> None:
        """Wait until the specified element is clickable

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: key corresponding to the element's locator in the
                page object's locators dictionary.
            timeout: seconds to wait for the element to be clickable or None.
                Default is set in the environment.py file.

        Raises:
            TimeoutException: if the element was not clickable after the
                timeout was reached

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            # Explicitly wait .3 seconds because
            # `wait_for_element_to_be_clickable` doesn't deterministically wait
            # long enough
            time.sleep(0.3)
            LOGGER.debug(
                f"Waiting for element {element_name} to be clickable on the page."
            )
            WebDriverWait(ctx.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            LOGGER.debug(f"Element {element_name} is now clickable on the page.")
        except TimeoutException:
            raise TimeoutException(
                f"The '{element_name}' element was not click-able when"
                " it was expected to be on the page."
            )

    @staticmethod
    def wait_for_text_to_change(
        ctx: Context,
        locators: dict,
        element_name: str,
        original_text: str,
        timeout: Union[int, None] = None,
    ) -> None:
        """Wait until the specified element's text doesn't match the given text

        Args:
            ctx: The behave context object
            locators: dict of element locators
            element_name: key corresponding to the element's locator in the
                page object's locators dictionary
            original_text: the original text of the element
            timeout: time in seconds to wait

        Raises:
            TimeoutException: if the element text still matches the given text
                after the timeout was reached

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Waiting for element {element_name} with original text: '{original_text}' to change."
            )
            WebDriverWait(ctx.driver, timeout).until(
                text_to_change(locator, original_text)
            )
        except TimeoutException:
            raise TimeoutException(
                f"The '{element_name}' element's text "
                f"was still '{original_text}' when it was expected to "
                "have changed"
            )

    @staticmethod
    def wait_for_presence_of_alert(
        ctx: Context, timeout: Union[int, None] = None
    ) -> None:
        timeout = timeout or ctx.wait_timeout
        try:
            LOGGER.debug("Waiting for the presence of an alert")
            WebDriverWait(ctx.driver, timeout).until(EC.alert_is_present())
        except TimeoutException:
            raise TimeoutException(
                f"The alert was not present when it" " was expected to be on the page."
            )
