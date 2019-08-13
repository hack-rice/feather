"""Script that evaluates applicants."""
from queue import Queue
from threading import Thread
from typing import Iterable

from scripts.constants import Constants
from feather.email import EmailDaemon, EndOfStreamPacket, EmailPacket
from feather.email.email_factory import EmailFactory
from feather import UnsubmittedUser


class RemindDaemon(Thread):
    def __init__(self, fac: EmailFactory, unsubmitted_users: Iterable[UnsubmittedUser], email_queue: "Queue") -> None:
        super().__init__(daemon=True)
        self.fac = fac
        self._unsubmitted_users = unsubmitted_users
        self._email_queue = email_queue

    def run(self) -> None:
        # schedule the emails
        for user in self._unsubmitted_users:
            email = self.fac.create_email("reminder.html", first_name="Hacker", email_subject="Hello!")
            email_packet = EmailPacket(user.email, email)
            self._email_queue.put(email_packet)

        self._email_queue.put(EndOfStreamPacket())


def _main() -> None:
    """Main function. (1) Asks the user for the name of a csv that contains applicant
    decisions. (2) Evaluates the applicants accordingly. (3) If there are any
    applicants whose decisions couldn't be parsed, create a new csv with only their
    information.
    """
    # retrieve users to email
    users = [
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com")
    ]
    fac = EmailFactory(Constants.TEMPLATES_PATH, Constants.EMAIL, Constants.EVENT_NAME)

    # create and start the email daemon
    message_queue = Queue()  # queue to communicate with email daemon
    consumer = EmailDaemon(Constants.EMAIL, Constants.EMAIL_PASSWORD, message_queue)
    producer = RemindDaemon(fac, users, message_queue)

    consumer.start()
    producer.start()

    # wait for emails to finish sending
    producer.join()
    consumer.join()


if __name__ == "__main__":
    _main()
