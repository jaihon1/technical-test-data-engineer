from logger import logger
from pydantic import ValidationError


class ApiValidator:
    def __init__(self, schema):
        """
        Initialize the validator with a Pydantic schema class.
        :param schema: Pydantic schema class used for validation (e.g., ApiSchema)
        """
        self.schema = schema

    def validate(self, response):
        """
        Validate the given response using the specified schema.
        :param response: The API response to validate
        :return: The validated response if successful, None otherwise
        """
        try:
            validated_response = self.schema(**response)
            return validated_response

        except ValidationError as e:
            logger.error(f"Validation failed: {e}")
            return None
