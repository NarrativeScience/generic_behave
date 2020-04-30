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

    @staticmethod
    def clear_text_by_index_in_list_of_elements(
        ctx: Context, locators: dict, element_name: str, element_index: int
    ) -> None:
        """
        Find an element from a list of elements using it's locator and the index
            of the element on the page

        Args:
            ctx: The behave context object.
            locators: dict of element locators.
            element_name: The key corresponding to the element's locator strategy
                in the page object's locators dictionary.
            element_index: The index the specific desired element should have

        """
        LOGGER.debug(f"Attempting to clear the {element_name} {element_index}")
        GeneralFunctions.get_elements_by_name(ctx, locators, element_name)[
            element_index
        ].clear()
