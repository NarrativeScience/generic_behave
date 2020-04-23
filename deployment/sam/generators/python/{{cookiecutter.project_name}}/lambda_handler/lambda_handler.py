{%- if cookiecutter.is_cf_custom_resource == "yes" -%}
import logging
import os

from ns_cf_custom_resources import CustomResourceHandler, resolve_secrets
from ns_python_logger.cli_logger import cli_logger

LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "INFO"))
logger = cli_logger("custom-resource", level=LOG_LEVEL)
logger.set_context()


class MyNewCustomResourceHandler(CustomResourceHandler):
    """Custom resource handler for Custom::MyNewResource"""

    RESOURCE_PROPERTIES_SCHEMA = {
        "type": "object",
        "properties": {
            "ServiceToken": {"type": "string"},
            # ...Include property definitions here...
            "MyProperty": {"type": "string"},
        },
        "required": [
            # Properties required for any custom resource
            "ServiceToken",
            # Properties required for this custom resource
            # ...Include required properties here...
            "MyProperty",
        ],
    }

    async def _handle_create(self) -> None:
        """Handler for the Create request type."""
        logger.info(f'MyProperty={self.event["ResourceProperties"]["MyProperty"]}')

    async def _handle_update(self) -> None:
        """Handler for the Update request type."""
        logger.info(
            f'Old MyProperty: {self.event["OldResourceProperties"]["MyProperty"]}'
        )
        logger.info(f'New MyProperty={self.event["ResourceProperties"]["MyProperty"]}')

    async def _handle_delete(self) -> None:
        """Handler for the Delete request type."""
        logger.info(
            f'Deleting! MyProperty={self.event["ResourceProperties"]["MyProperty"]}'
        )


def lambda_handler(event, context):
    """Lambda function handler"""
    return MyNewCustomResourceHandler(event).handle()
{% else -%}
import json
import logging
import os

from ns_python_core.enums import Directions
from ns_python_logger.cli_logger import cli_logger

LOG_LEVEL = getattr(logging, os.environ.get("LOG_LEVEL", "INFO"))
logger = cli_logger("{{ cookiecutter.project_name }}", level=LOG_LEVEL)
logger.set_context()


def lambda_handler(event, context):
    """Lambda function handler"""
    logger.info({"event": event})
    return {
        "statusCode": 200,
        "body": json.dumps({"message": f"Be {Directions.positive}"}),
    }


if __name__ == "__main__":
    print(lambda_handler(None, None))
{% endif -%}
