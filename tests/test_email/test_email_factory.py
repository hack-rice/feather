"""Test for the JinjaEmailFactory."""
import unittest
import os.path as path
from feather.email import JinjaEmailFactory


class TestJinjaEmailFactory(unittest.TestCase):
    """Unit test suite for the GmailClient."""
    def test_jinja_email_factory(self):
        fac = JinjaEmailFactory(path.dirname(path.abspath(__file__)), "HR Team")
        email = fac.create_email("Hello", "test_template.html", "", first_name="Hacker")

        self.assertEqual("HR Team", email.from_name)
        self.assertEqual("Hello", email.email_subject)
        self.assertEqual("Hacker", email.contents())
