# Custom WebDriver conditions. See the "Custom Wait Conditions" section of
# https://selenium-python.readthedocs.io/waits.html


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class element_not_present(object):
    """Wait until an element is not on the page"""

    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver) -> bool:
        """Return True if the element is not on the page, and False otherwise

        Instantiate a `presence_of_element_located` object with the locator of
        the element. Then, call the object's `__call__` method, which returns
        True if the given element is present on the page and raises a
        NoSuchElementException exception otherwise. Since we are expecting the
        element to not be present on the page, catch the error and return True.

        Args:
            driver: WebDriver object running the test

        Returns:
            Bool: False if the given element is present on the page, and True
                if it is present on the pages

        """
        try:
            element_located_call_method = EC.presence_of_element_located(self.locator)
            element_located_call_method(driver)
            return False
        except NoSuchElementException:
            return True


class text_to_change(object):
    """Wait until the given element's text does not match the given text"""

    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver) -> bool:
        """Find the element and compare its text attribute to the given text

        Args:
            driver: WebDriver object running the test

        Returns:
            bool: False if the element's text matches the given text, True if
                it does not match

        """
        element_located_call_method = EC.presence_of_element_located(self.locator)
        element = element_located_call_method(driver)
        actual_text = element.text
        return actual_text != self.text


class element_is_of_length(object):
    """Wait until the element's length matches the expected length"""

    def __init__(self, locator, expected_length):
        self.locator = locator
        self.expected_length = expected_length

    def __call__(self, driver) -> bool:
        """Find the element's length and compare it to the expected length

        Args:
            driver: WebDriver object running the test

        Returns:
            bool: True if the element's length matches the expected length,
                False if it does not match

        """
        elements_located_call_method = EC.presence_of_all_elements_located(self.locator)
        elements = elements_located_call_method(driver)
        actual_length = len(elements)
        return actual_length == self.expected_length
