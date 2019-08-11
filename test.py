"""Script that evaluates applicants."""
from queue import Queue

from feather.email import EmailDaemon, EndOfStreamPacket, EmailPacket


def _main() -> None:
    """Main function. (1) Asks the user for the name of a csv that contains applicant
    decisions. (2) Evaluates the applicants accordingly. (3) If there are any
    applicants whose decisions couldn't be parsed, create a new csv with only their
    information.
    """
    # make sure they actually want to do this
    followup_message = """
    Are you SURE that you want to do this? Running this script
    will email all registered users who haven't submitted their
    application. You cannot undo this.

    Proceed? (y/n): """
    response = input(followup_message)
    if response != "y":
        return

    # create and start the email daemon
    message_queue = Queue()  # queue to communicate with email daemon
    consumer = EmailDaemon(message_queue)
    consumer.start()

    # schedule the emails
    for _ in range(250):
        message_queue.put(
            EmailPacket("reminder.html", "HackRice 9 Application Deadline", "horeilly1101@gmail.com", "Boy")
        )

    message_queue.put(EndOfStreamPacket())

    # wait for emails to finish sending
    consumer.join()


if __name__ == "__main__":
    _main()
