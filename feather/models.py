"""File that contains various model objects."""
from collections import namedtuple

UnsubmittedUser = namedtuple("UnsubmittedUser", "id email")
UnsubmittedUser.__doc__ = """Namedtuple that represents a hackathon user who has
registered their account but hasn't yet submitted their application."""

Applicant = namedtuple("Applicant", "id email first_name last_name")
Applicant.__doc__ = """Namedtuple that represents a hackathon user who has 
submitted their application but hasn't yet been evaluated."""

Evaluation = namedtuple("Evaluation", "email first_name decision")
Evaluation.__doc__ = """Namedtuple that represents a hackathon user's 
evaluation."""
