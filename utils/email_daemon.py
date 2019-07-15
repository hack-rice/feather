
from threading import Thread
from queue import Queue
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import Config


def _send_email(server, applicant):
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = Config.EMAIL
    message["To"] = "horeilly1101@gmail.com"

    part1 = MIMEText("hey it's me", "text")
    message.attach(part1)

    server.sendmail(
        Config.EMAIL, "horeilly1101@gmail.com", message.as_string()
    )


class EmailDaemon(Thread):
    def __init__(self, queue: Queue) -> None:
        super().__init__(daemon=True)
        self.queue = queue

    def run(self) -> None:
        # we need the context to stay true for us to send mass emails
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(Config.EMAIL_HOST, 465, context=context) as server:
            server.login(Config.EMAIL, Config.EMAIL_PASSWORD)

            while True:
                applicant = self.queue.get()
                _send_email(server, applicant)
