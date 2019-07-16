"""File that contains various model objects."""
from collections import namedtuple

User = namedtuple("User", "id email first_name last_name")
User.__doc__ = """Namedtuple that represents a hackathon user."""

Evaluation = namedtuple("Evaluation", "email first_name decision")
Evaluation.__doc__ = """Namedtuple that represents a hackathon applicant's 
evaluation."""
