"""Package that contains the Feather API."""
import logging

# Configure the logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()

logger_format = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')
handler.setFormatter(logger_format)

LOGGER.addHandler(handler)
