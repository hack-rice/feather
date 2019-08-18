"""File that contains various converter functions to help us convert json objects
into our own model objects.
"""
from typing import Tuple
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


def parse_to_applicant(user_json, quill_base_url: str) -> Applicant:
    """Converter method that converts a user json object (as stored in quill's database)
    into an Applicant.

    :param user_json: User json object (as stored in quill's database)
    :param quill_base_url: the URL of your quill app (e.g. http://quill.herokuapp.com)
    :return: a Applicant model object
    """
    first_name, last_name = _split_name(user_json["profile"]["name"])
    user_id = user_json["_id"]
    school = user_json["profile"]["school"]
    team = None

    # this is how quill creates the profile links
    profile_link = f"{quill_base_url}/admin/users/{user_id}"
    return Applicant(
        user_json["email"],
        first_name,
        last_name,
        profile_link
    )


def parse_to_unsubmitted_user(user_json) -> UnsubmittedUser:
    """Converter method that converts a user json object (as stored in quill's database)
    into an UnsubmittedUser.

    :param user_json: User json object (as stored in quill's database)
    :return: an UnsubmittedUser model object
    """
    return UnsubmittedUser(user_json["_id"], user_json["email"])