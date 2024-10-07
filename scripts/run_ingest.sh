#!/bin/bash

# Export environment variables
export API_URL="http://localhost:8000"
export VERSION_ID=42
export REQUEST_SIZE=100
export DEV_MODE=true

# Run the moovitamix data flux application for different endpoints
export ENDPOINT="/users"
python -m src.data_flux.main

export ENDPOINT="/tracks"
python -m src.data_flux.main

export ENDPOINT="/listen_history"
python -m src.data_flux.main