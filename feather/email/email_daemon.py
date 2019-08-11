"""File that contains the EmailDaemon class."""
from threading import Thread
from queue import Queue
import smtplib
import ssl
import logging
import time

from constants import Constants
from feather.email.create_email import create_email

LOGGER = logging.getLogger(__name__)


def _get_server_connection():
    # create and secure server connection
    context = ssl.create_default_context()
    server = smtplib.SMTP(Constants.EMAIL_HOST, 587)
    server.starttls(context=context)

    # log in to your email
    server.login(Constants.EMAIL, Constants.EMAIL_PASSWORD)
    return server


class EmailDaemon(Thread):
    """Daemon that coordinates email campaigns."""
    def __init__(self, queue: Queue) -> None:
        super().__init__(daemon=True)
        self._queue = queue

        # store packets that aren't delivered
        self.undelivered_packets = []

    def run(self) -> None:
        """Run method for the EmailDaemon. This method listens on self._queue and sends
        an email when ordered to. The daemon will run until it receives an EndOfStreamPacket.
        """
        LOGGER.info("The EmailDaemon thread is starting.")

        # connect to the server
        server = _get_server_connection()

        while True:
            # block when the queue is empty
            data = self._queue.get()
            if data.stream_is_finished():
                break

            # create and send email
            mail = create_email(data.template_name, data.email_subject, data.email, data.first_name)
            try:
                server.sendmail(Constants.EMAIL, data.email, mail.as_string())
                LOGGER.info(f"Email sent to {data.email}. (template={data.template_name})")

                # sleep so as not to pass the gmail send limit
                time.sleep(2)

            except smtplib.SMTPException as e:
                LOGGER.error(f"Email to {data.email} failed to send due to an error.")
                LOGGER.error(e)
                self.undelivered_packets.append(data)

                # reconnect to server
                time.sleep(30)
                server = _get_server_connection()

        server.quit()  # end the connection
        LOGGER.info("The EmailDaemon thread is finished.")
