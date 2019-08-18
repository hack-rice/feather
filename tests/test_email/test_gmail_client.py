
import unittest
import unittest.mock as mock
import smtplib
from feather.email import GmailClient, Email


class SuccessfulGmailClient(GmailClient):
    def _get_server_connection(self) -> smtplib.SMTP:
        server = mock.Mock()

        def sendmail(from_addr, to_addrs, msg) -> None:
            pass
        server.sendmail = sendmail

        return server


class UnsuccessfulGmailClient(GmailClient):
    def _get_server_connection(self) -> smtplib.SMTP:
        server = mock.Mock()

        def sendmail(from_addr, to_addrs, msg):
            raise smtplib.SMTPRecipientsRefused(None)
        server.sendmail = sendmail

        return server


class TestGmailClient(unittest.TestCase):
    """Unit test suite for the GmailClient."""
    def test_success(self):
        client = SuccessfulGmailClient("fake@gmail.com", "XxhackricexX")
        with self.assertLogs(level="INFO") as cm:
            client.send_mail(
                "hack@rice.edu",
                Email("Hello", "HR", "<>"),
                success_wait_period=0,
                fail_wait_period=0
            )
            self.assertEqual(1, len(cm.output))
            self.assertEqual("INFO", cm.records[0].levelname)

    def test_failure(self):
        client = UnsuccessfulGmailClient("fake@gmail.com", "XxhackricexX")
        with self.assertLogs(level="ERROR") as cm:
            client.send_mail(
                "hack@rice.edu",
                Email("Hello", "HR", "<>"),
                success_wait_period=0,
                fail_wait_period=0
            )
            self.assertEqual(2, len(cm.output))
            self.assertEqual("ERROR", cm.records[0].levelname)

        self.assertEqual(1, len(client.undelivered_messages))
