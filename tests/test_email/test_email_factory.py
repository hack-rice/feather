"""Test for the GmailClient."""
import unittest
from feather.email import JinjaEmailFactory


class MockJinjaEmailFactory(JinjaEmailFactory):
    def _render_template(self, filename, first_name) -> str:
        return first_name


class TestGmailClient(unittest.TestCase):
    """Unit test suite for the GmailClient."""
    def test_jinja_email_factory(self):
        fac = MockJinjaEmailFactory(None, "HR Team")
        email = fac.create_email("Hello", "none.html", "Hacker")

        self.assertEqual("HR Team", email.from_name)
        self.assertEqual("Hello", email.email_subject)
        self.assertEqual("Hacker", email.contents())
