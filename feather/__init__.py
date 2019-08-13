"""Package that contains the Feather API."""
import logging

# API imports
from feather.dao import QuillDao
from feather.models import UnsubmittedUser, Applicant, Evaluation

# Configure the logger
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()

logger_format = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')
handler.setFormatter(logger_format)

_LOGGER.addHandler(handler)
