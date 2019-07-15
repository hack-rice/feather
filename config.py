"""File that contains necessary config information for the project."""

import os
from os import path

# load environment variables
from dotenv import load_dotenv
load_dotenv()

# absolute path of this file
PATH = path.dirname(path.abspath(__file__))


class Config:
    """Class that contains necessary config information."""
    # database info
    MONGODB_URI = os.environ["MONGODB_URI"]
    DB_NAME = os.environ["DB_NAME"]
    BASE_URL = os.environ["BASE_URL"]

    # email info
    EMAIL = os.environ["EMAIL"]
    EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
    EMAIL_HOST = os.environ["EMAIL_HOST"]

    # the directory all csv files will be written in
    OUTBOX_PATH = path.join(PATH, "outbox")

    # the directory all csv files will be read from
    INBOX_PATH = path.join(PATH, "inbox")

    # location of the email templates
    TEMPLATES_PATH = path.join(PATH, "templates")
