import logging

from behave.runner import Context
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from .general_functions import GeneralFunctions

LOGGER = logging.getLogger(__name__)


class ClickFunctions:
    """
    All selenium element click functions
    """

    @staticmethod
    def click_at(ctx: Context, locators: dict, element_name: str) -> None:
        """
        Moved the mouse to a location of an element and then clicks at that location

        Args:
            ctx: The behave context object
            locators: dict of locators
            element_name: key corresponding to the element's locator in the
            page object's locators dictionary

        Returns:
            None
        """
        LOGGER.debug(
            f"Attempting to move mouse to element: {element_name} and click it."
        )
        ActionChains(ctx.driver).move_to_element(
            GeneralFunctions.get_element_by_name(ctx, locators, element_name)
        ).click().perform()
        LOGGER.debug(
            f"Successfully moved mouse to element: {element_name} and clicked it."
        )

    @staticmethod
    def click_element(ctx: Context, element: WebElement) -> None:
        """Click the element.

        Args:
            ctx: The behave context object
            element: element to click

        Returns:
            None
        """
        LOGGER.debug("Attempting to click the element")
        element.click()
        LOGGER.debug("Successfully clicked the element")

    @staticmethod
    def click_element_by_name(ctx: Context, locators: dict, element_name: str) -> None:
        """
        Find an element using its locator from its page object. If the element
        is found click on it.

        Args:
            ctx: The behave context object
            locators: dict of locators
            element_name: The key corresponding to the element's locator strategy
            in the page object's locators dictionary.

        Returns:
            None

        Raises: :py:class:`.TimeoutException`: when the element can't be found
            using the given locator strategy.
        """
        LOGGER.debug(f"Attempting to click on {element_name}")
        GeneralFunctions.get_element_by_name(ctx, locators, element_name).click()
        LOGGER.debug(f"Successfully clicked on {element_name}")

    @staticmethod
    def double_click(ctx: Context, locators: dict, element_name: str) -> None:
        """
        Finds an element using its locator from its page object. If the element
        is found it double clicks on it.

        Args:
            ctx: The behave context object
            locators: dict of locators
            element_name: The key corresponding to the element's locator strategy
            in the page object's locators dictionary.

        Returns:
            None

        Raises: :py:class:`.TimeoutException`: when the element can't be found
            using the given locator strategy.
        """
        LOGGER.debug(f"Attempting to double click on {element_name}.")
        ActionChains(ctx.driver).double_click(
            GeneralFunctions.get_element_by_name(ctx, locators, element_name)
        ).perform()
        LOGGER.debug(f"Successfully double clicked on {element_name}.")

    @staticmethod
    def click_element_in_dropdown_menu(
        ctx: Context, locators: dict, button_name: str, element_name: str
    ) -> None:
        """
        Clicks a specified element in a dropdown list.

        Args:
            ctx: The behave context object
            locators: Dict of locators
            button_name: The unique name button to open the menu
            element_name: The element in the menu to click

        Returns:
            None
        """
        LOGGER.debug(
            f"Attempting to click element: {element_name} in dropdown menu: {button_name}."
        )
        ClickFunctions.click_element_by_name(ctx, locators, button_name)
        ClickFunctions.click_element_by_name(ctx, locators, element_name)
        LOGGER.debug(
            f"Successfully clicked element: {element_name} in dropdown menu: {button_name}."
        )
