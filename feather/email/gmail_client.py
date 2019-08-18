import smtplib
import ssl
import logging
import time
from typing import List, NamedTuple

from feather.email.email import Email

LOGGER = logging.getLogger(__name__)


class _UndeliveredMessage(NamedTuple):
    to_addrs: str
    email: Email


class GmailClient:
    def __init__(self, email_address: str, password: str, ):
        self._email_address = email_address
        self._password = password

        # store a connection to the server
        self._server = self._get_server_connection()

        # store a list of messages that weren't able to be delivered
        self.undelivered_messages: List[_UndeliveredMessage] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def _get_server_connection(self) -> smtplib.SMTP:
        # create and secure server connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=ssl.create_default_context())

        # log in to your email
        server.login(self._email_address, self._password)
        return server

    def send_mail(self, to_addrs: str, email: Email, success_wait_period=2, fail_wait_period=30) -> None:
        try:
            self._server.sendmail(from_addr=self._email_address, to_addrs=to_addrs, msg=email.render())
            LOGGER.info(f"Email sent to {to_addrs}.")

            # sleep so as not to pass the gmail send limit when used iteratively
            # not doing this will result in a 421, 4.7.0 error from the server
            time.sleep(success_wait_period)

        except smtplib.SMTPException as e:
            LOGGER.error(f"Email to {to_addrs} failed to send due to an error.")
            LOGGER.error(e)
            self.undelivered_messages.append(_UndeliveredMessage(to_addrs, email))

            # pause, then reconnect to server
            time.sleep(fail_wait_period)
            self._server = self._get_server_connection()

    def close_connection(self) -> None:
        self._server.quit()
