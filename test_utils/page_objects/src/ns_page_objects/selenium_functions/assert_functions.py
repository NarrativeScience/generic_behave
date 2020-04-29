import logging
from typing import Union

from behave.runner import Context
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
