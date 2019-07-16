
from typing import Iterator, Tuple

from pymongo import MongoClient

from config import Config
from utils.models import User, Evaluation


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
    """Converter method that converts a user json object (as stored in quill's database)
    into a User model.

    :param user_json: User json object (as stored in quill's database)
    :return: a User model object
    """
    first_name, last_name = _split_name(user_json["profile"]["name"])
    return User(user_json["_id"], user_json["email"], first_name, last_name)


class QuillDao:
    """Data access object for Quill's database. This class contains various methods that
    should be used to interact with the backend database. The database should not be
    directly queried outside of this class.
    """
    def __init__(self):
        """Initialize a QuillDao."""
        # connect to the database
        client = MongoClient(Config.MONGODB_URI)
        db = client[Config.DB_NAME]

        # store some collections
        self.users = db["users"]
        self.rejected_users = db["rejected_users"]

    # -------------------
    # Read methods
    # -------------------

    def get_unevaluated_applicants(self) -> Iterator[User]:
        """Getter method for applicants who have been evaluated.

        :return: an iterator of Users. This evaluates lazily, so the output is about as
            space efficient as we can hope for.
        """
        return (parse_to_user(user_json) for user_json in self.users.find()
                if user_json["status"]["completedProfile"]
                and not user_json["status"]["admitted"])

    # -------------------
    # Write methods
    # -------------------

    def accept_applicant(self, email: str):
        self.users.find_one_and_update(
            {"email": email},
            {"$set": {
                "admitted": True,
                "admittedBy": Config.EMAIL
            }}
        )

    def reject_applicant(self, email: str):
        # move the applicant's info to the rejected_users collection
        profile = self.users.find_one_and_delete({"email": email})
        self.rejected_users.insert_one(profile)

    def waitlist_applicant(self, email: str):
        # do nothing
        pass
