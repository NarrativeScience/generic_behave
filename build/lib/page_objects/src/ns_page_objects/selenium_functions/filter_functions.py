import logging
from typing import List

from selenium.webdriver.remote.webelement import WebElement

LOGGER = logging.getLogger(__name__)


class FilterFunctions:
    """
    All selenium element filter functions

    """

    @staticmethod
    def filter_elements_by_exact_text(
        elements: List[WebElement], text: str
    ) -> WebElement:
        """Filter a list of elements to those that match the given text.

        Args:
            elements: List of elements to filter.
            text: Text to filter the elements by.

        Returns:
            The first element that matches the given text.

        Raises:
            :py:class:`.AssertionError`: when no elements match the given text.

        """
        LOGGER.debug(f"Searching for elements that match text: '{text}'.")
        filtered_element_list = [
            element for element in elements if element.text == text
        ]
        number_of_matching_elements = len(filtered_element_list)
        assert (
            number_of_matching_elements > 0
        ), f"Did not find any elements with text {text}"
        if number_of_matching_elements > 1:
            LOGGER.debug(
                f"Found {number_of_matching_elements} elements matching text "
                f"'{text}', using the first "
                "one."
            )
        return filtered_element_list[0]

    @staticmethod
    def filter_and_click(elements: List[WebElement], text: str) -> None:
        """Filter a list of elements to those that contain the given text
        and then click on the first element that matches.

        Args:
            elements: List of elements to filter.
            text: Text to filter the elements by.

        Returns:
            None
        """
        FilterFunctions.filter_elements_by_exact_text(elements, text).click()

    @staticmethod
    def filter_elements_with_text(elements: List[WebElement], text: str) -> WebElement:
        """Filter a list of elements to those that contain the given text.

        Args:
            elements: List of elements to filter.
            text: Text to filter the elements by.

        Returns:
            The first element that contains the given text.

        Raises:
            :py:class:`.ValueError`: when no elements contain the given text.

        """
        LOGGER.debug(
            f"Searching for elements that have text or partial-text: '{text}'."
        )
        filtered_element_list = [
            element for element in elements if text in element.text
        ]
        number_of_matching_elements = len(filtered_element_list)
        if not number_of_matching_elements > 0:
            raise ValueError(f"Did not find any elements with text '{text}'")
        if number_of_matching_elements > 1:
            LOGGER.debug(
                f"Found {number_of_matching_elements} elements containing "
                f"text '{text}', using the first one."
            )
        return filtered_element_list[0]
