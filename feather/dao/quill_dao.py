"""File that contains the QuillDao class."""
from typing import Iterator
from pymongo import MongoClient

# import feather.dao.converters as converters
from feather.dao.converters import parse_to_unsubmitted_user, parse_to_applicant
from feather.models import Applicant, UnsubmittedUser


class QuillDao:
    """Data access object for Quill's database. This class contains various methods that
    should be used to interact with the backend database. The database should not be
    directly queried outside of this class.
    """
    def __init__(self, mongodb_uri: str, db_name: str) -> None:
        """Initialize a QuillDao."""
        # connect to the database
        client = MongoClient(mongodb_uri)
        db = client[db_name]

        # store some collections
        self._users = db["users"]

        # NOTE: this collection will be created if it does not already exist
        self._rejected_users = db["rejected_users"]

    # -------------------
    # Read methods
    # -------------------

    def get_applicants(self, quill_base_url: str = "YOUR_BASE_URL") -> Iterator[Applicant]:
        """Getter method for users who have submitted an application but haven't been
        evaluated.

        :param quill_base_url: the URL of your quill app (e.g. http://quill.herokuapp.com).
            Defaults to "YOUR_BASE_URL".
        :return: an iterator of SubmittedUsers. This evaluates lazily, so the output is
            about as space efficient as we can hope for.
        """
        return (parse_to_applicant(user_json, quill_base_url)
                for user_json in self._users.find()
                if user_json["status"]["completedProfile"]
                and not user_json["status"]["admitted"])

    def get_unsubmitted_users(self) -> Iterator[UnsubmittedUser]:
        """Getter method for users who have registered their account, but haven't
        submitted an application.

        :return: an iterator of UnsubmittedUsers. This evaluates lazily, so the output is
            about as space efficient as we can hope for.
        """
        return (parse_to_unsubmitted_user(user_json)
                for user_json in self._users.find()
                if user_json["verified"]
                and not user_json["status"]["completedProfile"])

    # -------------------
    # Write methods
    # -------------------

    def accept_applicant(self, email: str, accepted_by: str = "") -> None:
        """
        Accept an applicant to the hackathon. This function will (a) mark the applicant
        as admitted in the database and (b) note that they were admitted by the user whose
        email is set up in the .env file.

        :param email: the email of the applicant to be admitted
        :param accepted_by: the email of the user who is accepting the applicant. Defaults
            to the empty string.
        """
        self._users.find_one_and_update(
            {"email": email},
            {"$set": {
                "status.admitted": True,
                "status.admittedBy": accepted_by
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
