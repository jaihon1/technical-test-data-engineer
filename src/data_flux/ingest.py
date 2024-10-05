import asyncio
from logger import logger

from schema import ApiSchema
from validator import ApiValidator


class Ingest:
    def __init__(self, client):
        self.client = client
        self.data = None

    async def execute(self):
        tasks = []  # List to hold all fetch tasks

        for _ in range(10):
            # result = await fetch(url)
            tasks.append(self.client.fetch('/tracks', {'page':1, 'size':1}))

        # Run all tasks concurrently
        logger.info("Waiting for all request to be completed")

        # Wait for all fetched data to complete
        self.data = await asyncio.gather(*tasks)

        return self.data

    def validate(self):
        for response in self.data:
            logger.info(
                "Fetched data configs: Total={}, Page={}, Size={}, Pages={}", response['total'], response['page'], response['size'], response['pages']
            )

            validator = ApiValidator(ApiSchema)

            # response['items'][0]['id'] = '123'
            userapi_validated = validator.validate(response)

            logger.debug(userapi_validated)
