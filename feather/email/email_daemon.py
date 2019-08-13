"""File that contains the EmailDaemon class."""
from threading import Thread
from queue import Queue
import smtplib
import ssl
import logging
import time

from feather.email.data_packet import DataPacket

LOGGER = logging.getLogger(__name__)


class EmailDaemon(Thread):
    """Daemon that coordinates email campaigns."""
    def __init__(self, email_address: str, email_password: str, queue: "Queue[DataPacket]") -> None:
        super().__init__(daemon=True)
        self._email_address = email_address
        self._email_password = email_password
        self._queue = queue

        # store packets that aren't delivered
        self.undelivered_packets = []

    def _get_server_connection(self):
        # create and secure server connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=ssl.create_default_context())

        # log in to your email
        server.login(self._email_address, self._email_password)
        return server

    def run(self) -> None:
        """Run method for the EmailDaemon. This method listens on self._queue and sends
        an email when ordered to. The daemon will run until it receives an EndOfStreamPacket.
        """
        LOGGER.info("The EmailDaemon thread is starting.")

        # connect to the server
        server = self._get_server_connection()

        while True:
            data = self._queue.get()  # block when the queue is empty
            if data.stream_is_finished():
                break

            # create and send email
            mail_contents = data.email.render()
            try:
                server.sendmail(from_addr=self._email_address, to_addrs=data.to_email, msg=mail_contents)
                LOGGER.info(f"Email sent to {data.to_email}.")

                # sleep so as not to pass the gmail send limit
                # not doing this will result in a 421, 4.7.0 error from the server
                time.sleep(2)

            except smtplib.SMTPException as e:
                LOGGER.error(f"Email to {data.to_email} failed to send due to an error.")
                LOGGER.error(e)
                self.undelivered_packets.append(data)

                # reconnect to server
                time.sleep(30)
                server = self._get_server_connection()

        server.quit()  # end the connection
        LOGGER.info("The EmailDaemon thread is finished.")
