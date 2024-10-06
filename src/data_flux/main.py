import asyncio

from client import ClientAPI
from ingest import IngestManager
from logger import logger

async def main():
    logger.info("Data-Pipeline-Ingest module started")

    client = ClientAPI('http://localhost:8000')
    ingestManager = IngestManager(client, endpoint='/users')

    await ingestManager.configure(request_size=100)
    await ingestManager.run()


if __name__ == "__main__":
    asyncio.run(main())