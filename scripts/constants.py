"""File that contains necessary config information for the project."""
import os
from os import path

# load environment variables
from dotenv import load_dotenv
load_dotenv()

# absolute path of this file
_PATH = path.dirname(path.abspath(__file__))


class Constants:
    """Class that contains necessary config information."""
    # database info
    MONGODB_URI = os.environ["MONGODB_URI"]
    DB_NAME = os.environ["DB_NAME"]

    # email info
    EMAIL = os.environ["EMAIL"]
    EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

    # event info
    EVENT_NAME = os.environ["EVENT_NAME"]
    BASE_URL = os.environ["BASE_URL"]

    # the directory all csv files will be written in
    OUTBOX_PATH = path.join(_PATH, "outbox")

    # the directory all csv files will be read from
    INBOX_PATH = path.join(_PATH, "inbox")

    # location of the email templates
    TEMPLATES_PATH = path.join(_PATH, "templates")
