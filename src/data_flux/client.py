import aiohttp
from logger import logger


class ClientAPI:
    def __init__(self, base_url):
        """
        Initializes the ApiClient with a base URL.

        :param base_url: The base URL for the API (e.g., http://localhost:8000)
        """
        self.base_url = base_url

    async def fetch(self, endpoint, params=None):
        """
        Makes an HTTP GET request to the given endpoint with optional query parameters.

        :param endpoint: API endpoint (e.g., '/users', '/tracks' or '/listen_history')
        :param params: Dictionary of query parameters (e.g., {'page': 1, 'size': 3})
        :return: Response object or None if the request fails
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
