"""File that contains necessary config information for the project."""

import os

# load environment variables
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Class that contains necessary config information."""
    MONGODB_URI = os.environ["MONGODB_URI"]
    DB_NAME = os.environ["DB_NAME"]
    BASE_URL = os.environ["BASE_URL"]
