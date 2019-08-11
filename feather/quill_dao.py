"""File that contains the QuillDao class."""
from typing import Iterator, Tuple
from pymongo import MongoClient
from constants import Constants
from feather.models import Applicant, UnsubmittedUser


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


def parse_to_applicant(user_json) -> Applicant:
    """Converter method that converts a user json object (as stored in quill's database)
    into an Applicant.

    :param user_json: User json object (as stored in quill's database)
    :return: a Applicant model object
    """
    first_name, last_name = _split_name(user_json["profile"]["name"])
    return Applicant(user_json["_id"], user_json["email"], first_name, last_name)


def parse_to_unsubmitted_user(user_json) -> UnsubmittedUser:
    """Converter method that converts a user json object (as stored in quill's database)
    into an UnsubmittedUser.

    :param user_json: User json object (as stored in quill's database)
    :return: an UnsubmittedUser model object
    """
    return UnsubmittedUser(user_json["_id"], user_json["email"])


class QuillDao:
    """Data access object for Quill's database. This class contains various methods that
    should be used to interact with the backend database. The database should not be
    directly queried outside of this class.
    """
    def __init__(self):
        """Initialize a QuillDao."""
        # connect to the database
        client = MongoClient(Constants.MONGODB_URI)
        db = client[Constants.DB_NAME]

        # store some collections
        self._users = db["users"]

        # NOTE: this collection will be created if it does not already exist
        self._rejected_users = db["rejected_users"]

    # -------------------
    # Read methods
    # -------------------

    def get_applicants(self) -> Iterator[Applicant]:
        """Getter method for users who have submitted an application but haven't been
        evaluated.

        :return: an iterator of SubmittedUsers. This evaluates lazily, so the output is
            about as space efficient as we can hope for.
        """
        return (parse_to_applicant(user_json) for user_json in self._users.find()
                if user_json["status"]["completedProfile"]
                and not user_json["status"]["admitted"])

    def get_unsubmitted_users(self) -> Iterator[UnsubmittedUser]:
        """Getter method for users who have registered their account, but haven't
        submitted an application.

        :return: an iterator of UnsubmittedUsers. This evaluates lazily, so the output is
            about as space efficient as we can hope for.
        """
        return (parse_to_unsubmitted_user(user_json) for user_json in self._users.find()
                if user_json["verified"]
                and not user_json["status"]["completedProfile"])

    # -------------------
    # Write methods
    # -------------------

    def accept_applicant(self, email: str) -> None:
        """
        Accept an applicant to the hackathon. This function will (a) mark the applicant
        as admitted in the database and (b) note that they were admitted by the user whose
        email is set up in the .env file.

        :param email: the email of the applicant to be admitted
        """
        self._users.find_one_and_update(
            {"email": email},
            {"$set": {
                "admitted": True,
                "admittedBy": Constants.EMAIL
            }}
        )

    def reject_applicant(self, email: str) -> None:
        """
        Reject an applicant from the hackathon. This function will (a) delete the user
        from the database and (b) move all of their account information to the rejected_users
        collection in the database.

        This feels kind of hacky, because it means that rejected users will no longer be
        able to access their accounts. But as far as I can tell, this is the only way to
        reject users and maintain backwards compatibility with multiple versions of quill.

        :param email: the email of the applicant to be rejected
        """
        # move the applicant's info to the rejected_users collection
        profile = self._users.find_one_and_delete({"email": email})
        self._rejected_users.insert_one(profile)

    def waitlist_applicant(self, email: str) -> None:
        """
        Waitlist an applicant from the hackathon. This is a no op.
        :param email: the email of the applicant to be rejected.
        """
        # do nothing
        pass
