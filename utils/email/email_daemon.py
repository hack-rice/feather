"""File that contains the EmailDaemon class."""
from threading import Thread
from queue import Queue
import smtplib
import ssl

from config import Config
from utils.email.data_packet import EndOfStreamPacket
from utils.email.create_email import create_email


class EmailDaemon(Thread):
    """Daemon that coordinates email campaigns."""
    def __init__(self, queue: Queue) -> None:
        super().__init__(daemon=True)
        self._queue = queue

    def run(self) -> None:
        # start the server and log in to your email account
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(Config.EMAIL_HOST, 465, context=context) as server:
            server.login(Config.EMAIL, Config.EMAIL_PASSWORD)

            while True:
                data = self._queue.get()
                if isinstance(data, EndOfStreamPacket):
                    break

                # create and send email
                mail = create_email(None)
                server.sendmail(
                    Config.EMAIL, "horeilly1101@gmail.com", mail.as_string()
                )


if __name__ == "__main__":
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(Config.EMAIL_HOST, 465, context=context) as server:
        server.login(Config.EMAIL, Config.EMAIL_PASSWORD)

        email = create_email(None)
        server.sendmail(
            Config.EMAIL, "horeilly1101@gmail.com", email.as_string()
        )
