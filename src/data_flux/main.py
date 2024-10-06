import asyncio

from client import ClientAPI
from endpoints import Endpoints
from ingest import IngestManager
from logger import logger

async def main():
    logger.info("Data-Pipeline-Ingest module started")

    client = ClientAPI('http://localhost:8000')
    version_id = 11
    ingestManager = IngestManager(client, version_id=version_id, endpoint=Endpoints.USERS)

    await ingestManager.configure(request_size=100)
    await ingestManager.run(save=True)


if __name__ == "__main__":
    asyncio.run(main())