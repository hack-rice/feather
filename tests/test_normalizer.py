"""Test for the normalizer."""
import unittest
from feather.normalizer import ACCEPT, Normalizer


class TestNormalizer(unittest.TestCase):
    """Unit test suite for the Normalizer."""
    def test_accept(self):
        self.assertTrue(ACCEPT.matches("accept"))
        self.assertTrue(ACCEPT.matches("ACCEPT"))
        self.assertTrue(ACCEPT.matches("AccEpt"))
        self.assertTrue(ACCEPT.matches("Accept"))

    def test_not_accept(self):
        self.assertFalse(ACCEPT.matches("reject"))
        self.assertFalse(ACCEPT.matches("REJECT"))
        self.assertFalse(ACCEPT.matches("waitlist"))
        self.assertFalse(ACCEPT.matches("smthing"))

    def test_first_name(self):
        first_name = Normalizer("first name")
        self.assertTrue(first_name.matches("first name"))
        self.assertTrue(first_name.matches("firstname"))
        self.assertTrue(first_name.matches("First Name"))
        self.assertTrue(first_name.matches("First name"))
