import sys
from loguru import logger


# Configure the logger
logger.remove()

logger.add("logs/ingest_module.log",
           rotation="1 MB",
           level="INFO",
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
