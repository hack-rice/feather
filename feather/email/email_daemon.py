"""File that contains the EmailDaemon class."""
from threading import Thread
from queue import Queue
import smtplib
import ssl

from config import Config
from feather.email.data_packet import EndOfStreamPacket
from feather.email.create_email import create_email


class EmailDaemon(Thread):
    """Daemon that coordinates email campaigns."""
    def __init__(self, queue: Queue) -> None:
        super().__init__(daemon=True)
        self._queue = queue

    def run(self) -> None:
        """Run method for the EmailDaemon. This method listens on self._queue and sends
        an email when ordered to. The daemon will run until it receives an EndOfStreamPacket.
        """
        # start the server and log in to your email account
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(Config.EMAIL_HOST, 465, context=context) as server:
            server.login(Config.EMAIL, Config.EMAIL_PASSWORD)

            while True:
                # block when the queue is empty
                data = self._queue.get()
                if isinstance(data, EndOfStreamPacket):
                    break

                # create and send email
                mail = create_email(data.template_name, data.email_subject, data.email, data.first_name)
                server.sendmail(
                    Config.EMAIL, data.email, mail.as_string()
                )
