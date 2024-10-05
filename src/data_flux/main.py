import asyncio
import time

from client import ClientAPI
from ingest import Ingest
from logger import logger

async def main():
    logger.info("Data-Pipeline-Ingest module started")

    client = ClientAPI('http://localhost:8000')
    ingest = Ingest(client)

    logger.info("Fetching data...")

    start_time = time.time()  # Start the timer

    await ingest.execute()
    ingest.validate()

    elapsed_time = time.time() - start_time  # Calculate elapsed time

    logger.info("All fetches completed in {:.2f} seconds".format(elapsed_time))


# async def main():
#     logger.info("Data-Pipeline-Ingest module started")

#     url = 'http://localhost:8000/users?page=1&size=3'

#     try:
#         logger.info("Fetching data...")

#         start_time = time.time()  # Start the timer

#         for _ in range(1000):
#             result = await fetch(url)
#             logger.info("Data fetched successfully")
#             logger.debug("Fetched data: {}", result)


#         elapsed_time = time.time() - start_time  # Calculate elapsed time


#     except Exception as e:
#         logger.error("An error occurred: {}", e)

#     logger.info("All fetches completed in {:.2f} seconds".format(elapsed_time))


if __name__ == "__main__":
    asyncio.run(main())