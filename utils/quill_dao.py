
from typing import Iterator, Tuple
from collections import namedtuple

from pymongo import MongoClient

from config import Config


User = namedtuple("User", "id email first_name last_name")


def _split_name(name: str) -> Tuple[str, str]:
    """
    Split a name into two pieces--the first name, and everything that follows. If there are
    no spaces in the input name, the second element in the returned tuple will be the empty
    string.

    :param name: A person's name (e.g. "John Smith")
    :return: a 2-tuple with the person's first name as the first element, and everything
        else in the second element (e.g. tuple("John", "Smith"))
    """
    # split into two pieces at the first space
    names = name.split(" ", maxsplit=1)
    return names[0], names[1] if len(names) == 2 else ""


def parse_to_user(user_json) -> User:
    first_name, last_name = _split_name(user_json["profile"]["name"])
    return User(user_json["_id"], user_json["email"], first_name, last_name)


class QuillDao:
    """Class that represents the data access object for Quill's database."""
    def __init__(self):
        # connect to the database
        client = MongoClient(Config.MONGODB_URI)
        db = client[Config.DB_NAME]

        # store some collections
        self.users = db["users"]
        self.rejected_users = db["rejected_users"]

    def get_unevaluated_applicants(self) -> Iterator[User]:
        return (parse_to_user(user_json) for user_json in self.users.find()
                if user_json["status"]["completedProfile"]
                and not user_json["status"]["admitted"])
