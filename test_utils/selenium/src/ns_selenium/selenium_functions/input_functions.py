import logging

from behave.runner import Context

from .general_functions import GeneralFunctions

LOGGER = logging.getLogger(__name__)


class InputFunctions:
    """
    All selenium input functions
    """

    @staticmethod
    def send_keys_to_element_by_name(
        ctx: Context, locators: dict, element_name: str, keys_to_send: str
    ) -> None:
        """
        Find an element using its locator from its page object. If the element
        is found send keys to that element.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: The key corresponding to the element's locator strategy
            in the page object's locators dictionary.
            keys_to_send: The keys to send to the element. keys are in string format.

        Returns: None

        Raises: :py:class:`.TimeoutException`: when the element can't be found
            using the given locator strategy.
        """
        # Sending keys as ******* so we do not compromise passwords here
        LOGGER.debug(
            f"Attempting to send keys: '**********' to element '{element_name}'."
        )
        GeneralFunctions.get_element_by_name(ctx, locators, element_name).send_keys(
            keys_to_send
        )

    @staticmethod
    def clear_text_by_element_name(
        ctx: Context, locators: dict, element_name: str
    ) -> None:
        """
        Find an element using its locator from its page object. If the element
        is found clear it.

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: The key corresponding to the element's locator strategy
            in the page object's locators dictionary.

        Returns: None

        Raises: :py:class:`.TimeoutException`: when the element can't be found
            using the given locator strategy.
        """
        LOGGER.debug(f"Attempting to clear {element_name}")
        GeneralFunctions.get_element_by_name(ctx, locators, element_name).clear()
