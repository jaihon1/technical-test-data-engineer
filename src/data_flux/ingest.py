import asyncio
import math
import time
from logger import logger

from schema import ApiSchema
from validator import ApiValidator


class Ingest:
    def __init__(self, client, request_num=1):
        self.client = client
        self.request_num = request_num
        self.data = None


    async def execute(self, endpoint='/tracks', size=1):
        tasks = []  # List to hold all fetch tasks

        for page_num in range(1, self.request_num+1):
            logger.info(f"Requesting data from endpoint: {endpoint} with: page: {page_num}, size: {size}")
            tasks.append(self.client.fetch(endpoint, {'page': page_num, 'size': size}))

        # Run all tasks concurrently
        logger.info("Waiting for all request to be completed")

        # Wait for all fetched data to complete
        self.data = await asyncio.gather(*tasks)

        return self.data

    def validate(self):
        for response in self.data:
            # Requests that do not receive a valid response will have None values assigned to them.
            if response is None:
                logger.warning("Fetched data is invalid.")
                continue

            validator = ApiValidator(ApiSchema)
            # response['items'][0]['id'] = '123'
            userapi_validated = validator.validate(response)

            logger.debug(len(userapi_validated.items))


class IngestManager:
    def __init__(self, client, endpoint='/tracks'):
        self.client = client
        self.endpoint = endpoint

        self.ingest = None
        self.request_size = None
        self.request_num = None
        self.pages = None
        self.total = None

    async def configure(self, request_size=10, total=None):
        logger.info("Setting up IngestManager Configuration")
        logger.info(f"Testing connection endpoint: {self.endpoint}.")

        data = await self.client.fetch(self.endpoint, {'page': 1, 'size': request_size}) # Dummy values required for the request.

        if data == None:
            logger.error(f"Test connection failed for endpoint: {self.endpoint}. Aborting IngestManager configuration process.")
            raise ConnectionError

        logger.info(f"Successfuly called endpoint: {self.endpoint}.")

        validator = ApiValidator(ApiSchema)
        data_validated = validator.validate(data)

        self.pages = data_validated.pages
        self.total = data_validated.total if total is None else total
        self.request_size = request_size
        self.request_num = int(math.ceil(self.total / self.request_size))

        logger.info(f"Configuring Ingest with: Total: {self.total}, Request size: {self.request_size}, Number of requests: {self.request_num}")

        self.ingest = Ingest(self.client, request_num=self.request_num)

        logger.info("Successfuly setup of IngestManager Configuration")

    async def run(self):
        start_time = time.time()

        await self.ingest.execute(self.endpoint, self.request_size)
        self.ingest.validate()

        elapsed_time = time.time() - start_time

        # TODO: Have more redundant metrics. These metrics are good for now, but are not covering cases where some requests fail. Maybe have all requests tracked and from there we can see which ones were actually successful.
        logger.info(f"All fetches completed in {elapsed_time:.2f} seconds. Number of requests completed: {self.request_num}. Ingested {self.request_size*self.request_num} datapoints. Ingest throughput: {self.request_num/elapsed_time:.4f} req/s, {self.request_size*self.request_num/elapsed_time:.4f} datapoint/s")