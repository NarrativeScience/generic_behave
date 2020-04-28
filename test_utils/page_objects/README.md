# Page Objects

This python package is where all the selenium page objects reside.
Page objects are used as a dependency in the e2e tests as well as test selection and the e2e-linter.

## Adding a new page object

To add a new page object simply add a new python file with the standard name of <page_name>_page.py

All classes should extend the PageObject:

```python
from .page_object import PageObject

class AppsPage(PageObject):
    ...
```

All page object python files need to have a logger instantiated:

```python
import logging

LOGGER = logging.getLogger(__name__)
```

Additionally all page objects need to include a dict of locators:

```python
locators = {
        "add_app_button": (By.ID, "qa-add-app-button"),
}
```

### Adding locators:

Our standard order for adding/using locators in our page objects are as follows:
1. ID
1. Class Name
1. CSS Selector
1. XPATH

We avoid CSS and XPATH at all costs. If there is no ID or Class Name for a given element please find the element definition in the UI dev code and add an ID

The ID should begin with `qa_<...>` for easy identification that Software Test is using this in automation.
