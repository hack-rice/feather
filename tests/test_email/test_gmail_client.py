"""Test for the GmailClient."""
import unittest
import unittest.mock as mock
import smtplib
from feather.email import GmailClient, Email


class _SuccessfulGmailClient(GmailClient):
    def _get_server_connection(self) -> smtplib.SMTP:
        server = mock.Mock()

        def sendmail(from_addr, to_addrs, msg):
            pass
        server.sendmail = sendmail
        server.quit = lambda: None  # no op

        return server


class _UnsuccessfulGmailClient(GmailClient):
    def _get_server_connection(self) -> smtplib.SMTP:
        server = mock.Mock()

        def sendmail(from_addr, to_addrs, msg):
            raise smtplib.SMTPRecipientsRefused(None)
        server.sendmail = sendmail
        server.quit = lambda: None  # no op

        return server


class TestGmailClient(unittest.TestCase):
    """Unit test suite for the GmailClient."""
    def test_success(self):
        """Test sending a successful email with the client."""
        client = _SuccessfulGmailClient("fake@gmail.com", "XxhackricexX")
        with self.assertLogs(level="INFO") as cm:
            client.send_mail(
                "hack@rice.edu",
                Email("Hello", "HR", "", "<>"),
                success_wait_period=0,
                fail_wait_period=0
            )

            # we expect a single INFO message to be logged
            self.assertEqual(1, len(cm.output))
            self.assertEqual("INFO", cm.records[0].levelname)

    def test_failure(self):
        """Test sending an unsuccessful email with the client."""
        client = _UnsuccessfulGmailClient("fake@gmail.com", "XxhackricexX")
        with self.assertLogs(level="ERROR"):
            client.send_mail(
                "hack@rice.edu",
                Email("Hello", "HR", "", "<>"),
                success_wait_period=0,
                fail_wait_period=0
            )

        self.assertEqual(1, len(client.undelivered_messages))

    def test_context_manager(self):
        with _UnsuccessfulGmailClient("fake@gmail.com", "XxhackricexX") as client:
            client.send_mail(
                "hack@rice.edu",
                Email("Hello", "HR", "", "<>"),
                success_wait_period=0,
                fail_wait_period=0
            )

            self.assertEqual(1, len(client.undelivered_messages))
