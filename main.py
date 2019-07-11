"""main file"""
import os
from pprint import pprint
from pymongo import MongoClient


def _main():
    # load the environment variables
    from dotenv import load_dotenv
    load_dotenv()

    MONGODB_URI = os.environ["MONGODB_URI"]
    DB_NAME = os.environ["DB_NAME"]

    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]

    users = db["users"].find()

    for user in users:
        pprint(user)


if __name__ == "__main__":
    _main()
