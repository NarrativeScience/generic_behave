import logging
import re
from typing import Union

from behave.runner import Context
from ns_selenium.selenium_functions.general_functions import GeneralFunctions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

LOGGER = logging.getLogger(__name__)


class AssertFunctions:
    """
    All selenium assert functions
    """

    @staticmethod
    def element_is_present(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> bool:
        """
        Check if an element is present on a page. Wait the timeout and do not assert or throw
        and exception if the element is not found. Instead return False.

        Args:
            ctx: The behave context
            locators: Dictionary containing element locators for a page
            element_name: The element name to search for in the locators
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        Return:
            True if element is found, False if not.
        """
        # Set the timeout
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Checking to see if {element_name} is present on the page at {locator}"
            )
            # Check to see if the element is present in the DOM and visible on the page
            WebDriverWait(ctx.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            LOGGER.debug(f"Successfully found {element_name} on the page.")
            return True
        except TimeoutException:
            LOGGER.debug(f"Could not find {element_name} at {locator} on the page.")
            return False

    @staticmethod
    def element_is_not_present(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> bool:
        """
        Check if an element is not present on a page. Wait the timeout and do not assert or thrown
        an exception of the element is found. Instead return False

        Args
            ctx: The behave context
            locators: Dictionary containing element locators for a page
            element_name: The element name to search for in the locators
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        Return:
            True if element is not found, False if element is found.
        """
        # Set the timeout
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Checking to see if {element_name} is not present on the page at {locator}"
            )
            # Check to see if the element is not present in the DOM and not visible on the page
            WebDriverWait(ctx.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            LOGGER.debug(f"Did not find {element_name} at {locator} on the page.")
            return True
        except TimeoutException:
            LOGGER.debug(
                f"Found {element_name} on the page at {locator} and we did not expect to."
            )
            return False

    @staticmethod
    def validate_url_contains(ctx: Context, text: str) -> bool:
        """Validate the page url after navigating to a page from the sidebar

        Args:
            ctx: The behave context object
            text: The text that should be present in the url

        Return:
            True if the page url is found, False if not.

        """
        LOGGER.debug(f"Attempting to validate that the url contains: {text}")
        return True if text in ctx.driver.current_url else False

    @staticmethod
    def validate_page_url(ctx: Context, page_url_dict: dict, page_name: str) -> bool:
        """Validate the page url after navigating to a page from the sidebar

        Args:
            ctx: The behave context object
            page_url_dict: Dict of strings to match against the current url
            page_name: Common name of page to validate url of

        Return:
            True if the page url is found, False if not.

        """
        page_name_route = page_url_dict.get(page_name.lower(), "Invalid")
        LOGGER.debug(f"Attempting to validate that page url is: {page_name_route}")
        return AssertFunctions.validate_url_contains(ctx, page_name_route)

    @staticmethod
    def element_text_matches(
        ctx: Context,
        locators: dict,
        element_name: str,
        match_raw_str: str,
        timeout: Union[int, None] = None,
    ) -> bool:
        """
        Check if an element is present on a page. Wait the timeout and do not assert or throw
        and exception if the element is not found. Instead return False.

        Args:
            ctx: The behave context
            locators: Dictionary containing element locators for a page
            element_name: The element name to search for in the locators dict
            match_raw_str: The raw string used to match
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        Return:
            True if element is found, False if not.
        """
        # Set the timeout
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        try:
            LOGGER.debug(
                f"Checking to see if {element_name}'s text matches {match_raw_str}."
            )
            # Check to see if the element is present in the DOM and visible on the page
            WebDriverWait(ctx.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element_text = GeneralFunctions.get_elements_text_by_name(
                ctx, locators, element_name
            )
            re.match(match_raw_str, element_text)
            LOGGER.debug(
                f"Successfully matched {element_name}'s text to {match_raw_str}."
            )
            return True
        except TimeoutException:
            LOGGER.debug(f"Could not match {element_name}'s text to {match_raw_str}.")
            return False

    @staticmethod
    def validate_url_ends_with(ctx: Context, text: str) -> bool:
        """Validate that the url ends with specific text

            Args:
                ctx: The behave context
                text: The text with which the url should end

            Returns:
                A boolean representing whether or not the url ends with the given string

        """
        if not re.match(fr"{text}$", "/"):
            text += "/"
        return bool(re.match(fr"{text}$", ctx.driver.current_url))

    @staticmethod
    def element_is_active(
        ctx: Context,
        locators: dict,
        element_name: str,
        timeout: Union[int, None] = None,
    ) -> bool:
        """Obtain a boolean representing if an element is enabled

        Args:
            ctx: The behave context
            locators: Dictionary containing element locators for a page
            element_name: The element name to search for in the locators dict
            timeout: seconds to wait for the element to appear or None.
                Default is set in the environment.py file.

        """
        timeout = timeout or ctx.wait_timeout
        locator = locators[element_name]
        WebDriverWait(ctx.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element_status = GeneralFunctions.get_element_status(
            ctx, locators, element_name
        )
        return bool(element_status)
