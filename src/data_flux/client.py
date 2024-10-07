import aiohttp
from src.data_flux.logger import logger


class ClientAPI:
    def __init__(self, base_url):
        """
        Initializes the ClientAPI with a base URL.

        This constructor sets the base URL for the API, which will be used
        as a prefix for all API requests made through the client.

        Arguments:
            base_url (str):
                The base URL for the API (e.g., http://localhost:8000).
                This field is required for making requests.

        Returns:
            None
        """
        self.base_url = base_url

    async def fetch(self, endpoint, params=None):
        """
        Makes an HTTP GET request to the specified endpoint with optional query parameters.

        This method constructs the full URL by combining the base URL and the provided endpoint,
        and sends a GET request to the server. If the request is successful, it returns the JSON
        response. If the request fails, it logs the error and returns None.

        Arguments:
            endpoint (str):
                The API endpoint to fetch data from (e.g., '/users', '/tracks', or '/listen_history').
                This field is required.

            params (Optional[dict]):
                A dictionary of query parameters to include in the request (e.g., {'page': 1, 'size': 3}).
                Defaults to None if no parameters are needed.

        Returns:
            Optional[dict]:
                The JSON response from the API if the request is successful; otherwise, returns None.
        """

        url = f"{self.base_url}{endpoint}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()  # Raise an exception for 4XX/5XX errors

                    return await response.json()

            except Exception as e:
                logger.error(f"Error making request to {url} with {params}: {e}")

                return None
