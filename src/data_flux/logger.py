import os
import sys
from loguru import logger


# Configure the logger
is_dev_mode = os.getenv('DEV_MODE', 'false').lower() == 'true'

# Set the logging level based on the dev_mode
file_log_level = "DEBUG" if is_dev_mode else "INFO"

# Remove default handlers
logger.remove()

# Add file handler for logs
logger.add("logs/ingest_module.log",
           rotation="1 MB",
           level=file_log_level,
           format="{time} {level} {message}",
           compression="zip",
           enqueue=True
)

# Add console handler for debugging (logs to stdout)
logger.add(
    sys.stdout,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>",
    colorize=True
)
