from src.data_flux.logger import logger
from pydantic import ValidationError


class ApiValidator:
    """
    Validator class for API responses using Pydantic schemas.

    This class provides functionality to validate API responses against a specified
    Pydantic schema. It ensures that the structure and types of the response data
    conform to the expectations defined in the schema.

    Attributes:
        schema (BaseModel):
            A Pydantic schema class used for validating API responses (e.g., ApiSchema).
            This field is required for the validation process.

    Arguments:
        schema (BaseModel):
            The Pydantic schema class to be used for validation.
            This field is required for initializing the validator.
    """

    def __init__(self, schema):
        """
        Initialize the validator with a Pydantic schema class.

        Arguments:
            schema (ApiSchema):
                An instance of ApiSchema class.
                This field is required for initializing the validator.
        """
        self.schema = schema

    def validate(self, response):
        """
        Validate the given response using the specified schema.

        This method attempts to validate the provided API response against the
        initialized schema. If the validation is successful, it returns the validated
        response as an instance of the schema. If validation fails, it logs the error
        and returns None.

        Arguments:
            response (dict):
                The API response to validate, expected to match the schema's structure.

        Returns:
            Optional[ApiSchema]:
                The validated response as an instance of the ApiSchema if successful;
                otherwise, returns None.
        """
        try:
            validated_response = self.schema(**response)
            return validated_response

        except ValidationError as e:
            logger.error(f"Validation failed: {e}")
            return None