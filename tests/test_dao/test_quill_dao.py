"""Test for the GmailClient."""
import unittest
from unittest.mock import Mock
from feather import QuillDao


_TEST_USERS = [
    {
        "_id": "abc123",
        "email": "hack@rice.edu",
        "verified": True,
        "profile": {
            "name": "Hugh O'Reilly",
            "school": "Rice University"
        },
        "status": {
            "completedProfile": True,
            "admitted": True
        }
    },
    {
        "_id": "def456",
        "email": "hjo2@rice.edu",
        "verified": True,
        "status": {
            "completedProfile": False,
            "admitted": False
        }
    },
    {
        "_id": "fdasfsa",
        "email": "amc30@rice.edu",
        "verified": False,
        "status": {
            "completedProfile": False,
            "admitted": False
        }
    },
    {
        "_id": "123abc",
        "email": "john@mit.edu",
        "verified": True,
        "profile": {
            "name": "John John John Doe",
            "school": "Massachusetts Institute of Technology"
        },
        "status": {
            "completedProfile": True,
            "admitted": False
        }
    },
    {
        "_id": "ghj564",
        "email": "kesh@wustl.edu",
        "verified": True,
        "profile": {
            "name": "Keshav Kailash",
            "school": "Washington University in St. Louis"
        },
        "status": {
            "completedProfile": True,
            "admitted": False
        }
    },
]

_TEST_REJECTED_USERS = [
    {
        "_id": "fqrgqwgrqwe",
        "email": "jane@mit.edu",
        "verified": True,
        "profile": {
            "name": "Jane John John Doe",
            "school": "Massachusetts Institute of Technology"
        },
        "status": {
            "completedProfile": True,
            "admitted": False
        }
    },
    {
        "_id": "fefdasfs",
        "email": "joe@wustl.edu",
        "verified": True,
        "profile": {
            "name": "Joseph Kailash",
            "school": "Washington University in St. Louis"
        },
        "status": {
            "completedProfile": True,
            "admitted": False
        }
    },
]


class _MockQuillDao(QuillDao):
    def __init__(self):
        # don't call super!
        # we don't want to touch the MongoClient when testing
        self._users = Mock()
        self._users.find = lambda: _TEST_USERS

        self._rejected_users = Mock()
        self._rejected_users.find = lambda: _TEST_REJECTED_USERS


class TestQuillDao(unittest.TestCase):
    """Unit test suite for the QuillDao."""
    def test_get_applicants(self):
        dao = _MockQuillDao()
        applicants = list(dao.get_applicants("http://example.com"))  # convert iterator to list
        self.assertEqual(2, len(applicants))

        first_applicant = applicants[0]
        self.assertEqual("John", first_applicant.first_name)
        self.assertEqual("John John Doe", first_applicant.last_name)
        self.assertEqual("john@mit.edu", first_applicant.email)

        second_applicant = applicants[1]
        self.assertEqual("Keshav", second_applicant.first_name)
        self.assertEqual("http://example.com/admin/users/ghj564", second_applicant.profile_link)

    def test_get_unsubmitted_users(self):
        dao = _MockQuillDao()
        unsubmitted_users = list(dao.get_unsubmitted_users())  # convert iterator to list
        self.assertEqual(1, len(unsubmitted_users))

        first_unsubmitted_user = unsubmitted_users[0]
        self.assertEqual("hjo2@rice.edu", first_unsubmitted_user.email)
