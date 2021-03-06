import logging

from behave.runner import Context
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from ns_selenium.selenium_functions.general_functions import GeneralFunctions

LOGGER = logging.getLogger(__name__)


class ClickFunctions:
    """
    All selenium element click functions
    """

    @staticmethod
    def click_at_element_by_name(ctx: Context, locators: dict, element_name: str) -> None:
        """
        Moves the mouse to the location of an element by name, and then double clicks at
        that location.  This is for use in the case of transparent overlays that
        block the standard click element functions.  This should always be followed
        by a validation that the click did what was intended as this is a blind click.

        Args:
            ctx: The behave context object.
            locators: Dict of locators.
            element_name: Key corresponding to the element's locator in the
            page object's locators dictionary.

        Returns:
            None
        """
        LOGGER.debug(
            f"Attempting to move mouse to element: {element_name} and click it."
        )
        ActionChains(ctx.driver).move_to_element(
            GeneralFunctions.get_element_by_name(ctx, locators, element_name)
        ).double_click().perform()
        LOGGER.debug(
            f"Successfully moved mouse to element: {element_name} and clicked it."
        )

    @staticmethod
    def click_at_element(ctx: Context, element: WebElement) -> None:
        """
        Moves the mouse to the location of an element, and then clicks at
        that location.  This is for use in the case of transparent overlays that
        block the standard click element functions.  This should always be followed
        by a validation that the click did what was intended as this is a blind click.

        Args:
            ctx: The behave context object.
            element: The element to click.

        Returns:
            None
        """
        LOGGER.debug(
            f"Attempting to move mouse to element and click it."
        )
        ActionChains(ctx.driver).move_to_element(element).click().perform()
        LOGGER.debug(
            f"Successfully moved mouse to element and clicked it."
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
    def drag_and_drop(
            element_to_drag: WebElement, x_offset: int, y_offset: int
    ) -> None:
        """
        Drag and drop an element

        Args:
            element_to_drag: the element to be dragged
            x_offset: X offset to move to.
            y_offset: Y offset to move to.

        """
        LOGGER.debug(
            f'Attempting to drag and drop element to offset: {x_offset}, {y_offset}.'
        )
        ActionChains.drag_and_drop_by_offset(element_to_drag, x_offset, y_offset)
        LOGGER.debug(
            f'Successfully dragged and dropped element to offset: {x_offset}, {y_offset}.'
        )

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
