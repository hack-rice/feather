"""File that contains various model objects."""
from typing import NamedTuple


class UnsubmittedUser(NamedTuple):
    """Namedtuple that represents a hackathon user who has
    registered their account but hasn't yet submitted their application.
    """
    id: str
    email: str


class Applicant(NamedTuple):
    """Namedtuple that represents a hackathon user who has
    submitted their application but hasn't yet been evaluated.
    """
    email: str
    first_name: str
    last_name: str
    profile_link: str


class Evaluation(NamedTuple):
    """Namedtuple that represents a hackathon user's evaluation."""
    email: str
    first_name: str
    decision: str
