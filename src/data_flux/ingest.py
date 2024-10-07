import asyncio
import math
import time

from src.data_flux.endpoints import Endpoints
from src.data_flux.logger import logger

from src.data_flux.api_schema import ApiSchema
from src.data_flux.data_schema import endpoint_builder_map
from src.data_flux.validator import ApiValidator


class Ingest:
    """
    Class for ingesting data through a specified client.

    This class handles the process of ingesting batch data asynchronously using a provided client. It manages
    the number of requests and stores both raw and validated data during the ingestion
    process.
    """

    def __init__(self, client, validator, request_num=1):
        self.client = client
        self.validator = validator
        self.request_num = request_num
        self.data_raw = []
        self.data_validated = []


    async def execute(self, endpoint, size=1, start_page=1):
        """
        Execute concurrent I/O bound requests to the specified API endpoint.

        This method sends multiple asynchronous requests to the given API endpoint,
        retrieving data in pages. It constructs a list of tasks for each page request
        and executes them concurrently. The results are gathered and stored as raw
        data for further processing.

        Arguments:
            endpoint (str):
                The API endpoint to fetch data from (e.g., '/users', '/tracks').
                This field is required.

            size (int, optional):
                The number of items to retrieve per request. Defaults to 1 if not specified.

            start_page (int, optional):
                The page number it should start its execution. Defaults to 1 if not specified.

        Returns:
            list:
                A list containing the raw data fetched from the API. Each entry in the list
                corresponds to the data retrieved from each page request.
        """

        # List to hold all fetch tasks
        tasks = []

        # Execute all tasks concurrently
        for page_num in range(start_page, self.request_num+1):
            logger.info(f"Requesting data from endpoint: {endpoint} with: page: {page_num}, size: {size}")
            tasks.append(self.client.fetch(endpoint, {'page': page_num, 'size': size}))

        logger.info("Waiting for all request to be completed...")

        # Wait for all fetched data to complete
        self.data_raw = await asyncio.gather(*tasks)

        return self.data_raw

    def validate(self):
        """
        Validate the fetched raw data against the specified schema.

        This method iterates over the raw data collected from API responses, validating each
        response using the defined Pydantic schema. It logs warnings for invalid responses
        and extends the validated data list with valid items. The method also logs the number
        of items validated for debugging purposes.

        Process:
            - Iterates through each response in the raw data.
            - Checks if the response is None, log an invalid response.
            - Validates responses using the ApiValidator.
            - Builds the validated batch data.
            - Logs data about validated items for debugging.

        Returns:
            None
        """

        for response in self.data_raw:
            # Requests that do not receive a valid response will have None values assigned to them.
            if response is None:
                logger.warning("Fetched data is invalid.")
                continue

            validated = self.validator.validate(response)

            # Build batch dataset
            self.data_validated.extend(validated.items)

            # Log the number of items and their details
            if self.data_validated:
                logger.debug(f"Validated {len(self.data_validated)} items.")
                logger.debug(f"Example validated item: {self.data_validated[0]}.")
            else:
                logger.info(f"No validated items found. Please check the validation process.")



class IngestManager:
    """
    Class for managing the configuration and operation of data ingestion from a specified API endpoint.

    This class is responsible for configuring the ingestion process by fetching
    initial data from the API, validating it, and setting up the necessary parameters
    for data ingestion. It automatically uses the provided client to interact with the API and manages
    the number of requests needed based on the total data available.
    """

    def __init__(self, client, version_id, endpoint=Endpoints.USERS):
        self.client = client
        self.version_id = version_id
        self.endpoint = endpoint

        self.ingest = None
        self.request_size = None
        self.request_num = None
        self.pages = None
        self.total = None

    async def configure(self, request_size=10, total=None):
        """
        Configure the IngestManager by fetching and validating initial data from the API.

        This method tests the connection to the specified endpoint by making a request
        to fetch initial data. It automatically validates the response and calculates the number of requests
        required based on the total data available.

        Arguments:
            request_size (int, optional):
                The number of items to retrieve per request. Defaults to 10 if not specified.

            total (Optional[int]):
                The total number of items available for the API response (can be used to limit the request batch size to a certain size).
                If None, will be fetched from the API.

        Returns:
            None
        """

        logger.info(f"Configuring IngestManager.")
        logger.info(f"Testing connection to endpoint: {self.endpoint.value}.")

        data = await self.client.fetch(self.endpoint.value, {'page': 1, 'size': request_size}) # Dummy values required for the request.

        if data == None:
            logger.error(f"Test connection failed for endpoint: {self.endpoint.value}. Aborting IngestManager configuration process.")
            raise ConnectionError

        logger.info(f"Successfuly tested connection to endpoint: {self.endpoint.value}.")

        validator = ApiValidator(ApiSchema)
        data_validated = validator.validate(data)

        self.pages = data_validated.pages
        self.total = data_validated.total if total is None else total
        self.request_size = request_size
        self.request_num = int(math.ceil(self.total / self.request_size))

        logger.info(f"Configuring Ingest with: Total: {self.total}, Request size: {self.request_size}, Number of requests: {self.request_num}")

        self.ingest = Ingest(self.client, validator=validator, request_num=self.request_num)

        logger.info("Successfuly setup and configured IngestManager. IngestManager is ready to be used!")

    async def run(self, save=False):
        """
        Executes the data retrieval and validation process,
        and optionally saves the ingested data to a specified storage location.

        This method triggers the ingestion process by fetching data from the API endpoint,
        validating the responses, and logging the performance metrics. If the `save` parameter
        is set to True, it proceeds to map the validated data to the appropriate data schema
        for persistence.

        Arguments:
            save (bool, optional):
                A flag indicating whether to save the ingested data. Defaults to False.

        Returns:
            None
        """

        start_time = time.time()

        # Executes the data retreival and validation in batch of requests asynchronously
        await self.ingest.execute(self.endpoint.value, self.request_size)

        # Validates the feteched raw data
        self.ingest.validate()

        elapsed_time = time.time() - start_time

        # TODO: Have more redundant metrics. These metrics are good for now, but are not covering cases where some requests fail. Maybe have all requests tracked and from there we can see which ones were actually successful.
        logger.info(f"All fetches completed in {elapsed_time:.2f} seconds. Number of requests completed: {self.request_num}. Ingested {self.request_size*self.request_num} datapoints. Ingest throughput: {self.request_num/elapsed_time:.4f} req/s, {self.request_size*self.request_num/elapsed_time:.4f} datapoint/s")

        if save:
            logger.info(f"Saving ingested data: {len(self.ingest.data_validated)}")
            logger.info(f"Dataset size: {len(self.ingest.data_validated)}")

            # Dynamically find the proper mapping function
            build_function = endpoint_builder_map.get(self.endpoint)

            if build_function is None:
                raise ValueError(f"No build function found for endpoint: {self.endpoint}")

            # Mapping validated data to DataSchema used when persisting the data
            data_to_persist = [build_function(data, self.version_id) for data in self.ingest.data_validated]

            # Log a sample of the dataset
            if data_to_persist:
                logger.debug(f"Example of a validated and mapped item ready to be saved to storage: {data_to_persist[0]}.")
            else:
                logger.info(f"No validated items to persist. Ensure that the data ingestion process was successful.")

            # TODO: Here goes the interface for inserting data to a data store location