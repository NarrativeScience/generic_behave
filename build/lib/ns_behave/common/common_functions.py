"""Module holds additional generic helper functions for data manipulation."""

import base64
from datetime import datetime
import json
import logging
import random
import string

import boto3
from botocore.exceptions import ClientError

# Initialize a logger
LOGGER = logging.getLogger(__name__)


class Common:
    """Class of common functions for all of test_utils"""

    @staticmethod
    def gen_random_float(max_range: float) -> float:
        """Function that will generate a random float between zero and the given upper value.

        Args:
            max_range: The desired upper value of the number

        Returns:
            A random float between zero and the given upper value

        """
        return round(random.uniform(0.0, float(max_range)), 2)

    @staticmethod
    def gen_random_string(length: int) -> str:
        """Function that will generate a random string with a length defined by its input integer.

        Args:
            length: the length of the desired random string

        Returns:
            a random string using ascii_lowercase characters

        """
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    @staticmethod
    def gen_random_email(length: int) -> str:
        """Function that will generate a random email address.

        The email address itself will be the length defined by the int argument. This does not include the @domain.

        Args:
            length: the length of the desired email string

        Returns:
            a random email string using ascii_lowercase characters @narrativescience.com

        """
        return f"test_{Common.gen_random_string(length)}@narrativescience.com"

    @staticmethod
    def is_random_value(value: str) -> str:
        """Function that will check if there is a random x value denoted in a gherkin input.

        If so replace it with the requested random.
        If the string value read in is None at the start -> return None.

        Args:
            value: The value to check to see if we need replaced

        Return:
            The replaced random value

        """
        if value is None:
            return None
        else:
            # do we want a random int? If so gen one from 1-9
            if value == "{random int}":
                return str(random.randint(1, 9))
            # do we want a random date? If so gen one from the current date
            elif value == "{random date}":
                date = datetime.now()
                return date.strftime("%m/%d/%Y")
            # return the original value as we do not support that type of random
            else:
                return value

    @staticmethod
    def is_float(input_string: str) -> bool:
        """Function to determine if a string contains a float or not.

        Used for request bodies that need decimal values.

        Args:
            input_string: input string

        Returns:
            True or False if the input is a float

        """
        try:
            float(input_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_secret(secret_name: str, secret_key: str) -> str:
        """Gets a secret key from AWS Secrets Manager based on the secret_name.

        Args:
            secret_name: AWS secret name
            secret_key: Key to the value in the secret

        Return:
            the decoded secret string value

        """
        region_name = "us-east-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                LOGGER.error(f"Error decrypting secret: {str(e)}")
            elif e.response["Error"]["Code"] == "InternalServiceErrorException":
                LOGGER.error(
                    f"Internal service error while trying to fetch secret value"
                )
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                LOGGER.error(f"The requested secret {secret_name} was not found")
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                LOGGER.error(f"The request was invalid due to: {str(e)}")
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                LOGGER.error(f"The request had invalid params: {str(e)}")
            else:
                LOGGER.error(f"The request failed: {str(e)}")
            raise
        else:
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
            else:
                secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        return json.loads(secret)[secret_key]
