import asyncio
import os

from src.data_flux.client import ClientAPI
from src.data_flux.endpoints import Endpoints
from src.data_flux.ingest import IngestManager


async def main():
    url = os.getenv('API_URL', 'http://localhost:8000')  # Default to 'http://localhost:8000' if not set
    version_id = int(os.getenv('VERSION_ID', 11))        # Default to 11 if not set
    endpoint_str = os.getenv('ENDPOINT', '/users')       # Default to '/users' if not set
    request_size = int(os.getenv('REQUEST_SIZE', 100))   # Default to 100 if not set

    # Configure and convert the endpoint string to the Enum value
    try:
        endpoint = Endpoints(endpoint_str)
    except ValueError:
        raise ValueError(f"Invalid endpoint '{endpoint_str}'. Valid options are: {[e.value for e in Endpoints]}")

    # Build Client and IngestManager
    client = ClientAPI(url)
    ingestManager = IngestManager(client, version_id=version_id, endpoint=endpoint)

    # Configure and run IngestManager
    await ingestManager.configure(request_size=request_size)
    await ingestManager.run(save=True)


if __name__ == "__main__":
    asyncio.run(main())