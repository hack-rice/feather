"""File that contains various model objects."""
from dataclasses import dataclass


@dataclass
class UnsubmittedUser:
    """Namedtuple that represents a hackathon user who has
    registered their account but hasn't yet submitted their application.
    """
    id: str
    email: str


@dataclass
class Applicant:
    """Namedtuple that represents a hackathon user who has
    submitted their application but hasn't yet been evaluated.
    """
    email: str
    # school: str
    first_name: str
    last_name: str
    # team: str
    profile_link: str


@dataclass
class Evaluation:
    """Namedtuple that represents a hackathon user's evaluation."""
    email: str
    first_name: str
    decision: str


@dataclass
class Reimbursement:
    """Namedtuple that represents a hackathon user's reimbursement info."""
    email: str
    first_name: str
    address: str
    amount: str


@dataclass
class Attendee:
    """
    Namedtuple that represents a hacker that attended the event. MLH requests
    this information on each user after the event.
    """
    email: str
    name: str
    phone_number: str
    school: str
