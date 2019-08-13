"""Script that evaluates applicants."""
import logging
from queue import Queue
from threading import Thread
from typing import Iterable

from scripts.constants import Constants
from feather import Evaluation, QuillDao
from feather.email import EndOfStreamPacket, EmailPacket, EmailDaemon
from feather.csv import read_evaluated_users, write_evaluations_to_csv

# Configure the logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()

logger_format = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')
handler.setFormatter(logger_format)

LOGGER.addHandler(handler)

# configure the email subject for all of our emails
EMAIL_SUBJECT = f"{Constants.EVENT_NAME} Application Decision"


class EvaluateDaemon(Thread):
    """A daemon thread that evaluates hackathon applicants."""
    def __init__(self, evaluations: Iterable[Evaluation], email_queue: "Queue") -> None:
        super().__init__(daemon=True)
        self._evaluations = evaluations
        self._email_queue = email_queue

        # store evaluations that couldn't be parsed
        self.unparsed_evaluations = set()

    def run(self) -> None:
        LOGGER.info("The EvaluateDaemon thread is starting.")
        dao = QuillDao()

        for evaluation in self._evaluations:
            # --------------------
            # update database and queue email
            # --------------------

            if evaluation.decision == "reject":
                dao.reject_applicant(evaluation.email)
                LOGGER.info(f"{evaluation.first_name}({evaluation.email}) has been rejected.")

                self._email_queue.put(
                    EmailPacket("reject.html", EMAIL_SUBJECT, evaluation.email, evaluation.first_name)
                )

            elif evaluation.decision == "accept":
                dao.accept_applicant(evaluation.email)
                LOGGER.info(f"{evaluation.first_name}({evaluation.email}) has been accepted.")

                self._email_queue.put(
                    EmailPacket("accept.html", EMAIL_SUBJECT, evaluation.email, evaluation.first_name)
                )

            elif evaluation.decision == "waitlist":
                dao.waitlist_applicant(evaluation.email)
                LOGGER.info(f"{evaluation.first_name}({evaluation.email}) has been waitlisted.")

                self._email_queue.put(
                    EmailPacket("waitlist.html", EMAIL_SUBJECT, evaluation.email, evaluation.first_name)
                )

            # --------------------
            # store unparsed evaluations
            # --------------------

            else:
                LOGGER.info(f"Unable to parse {evaluation.first_name}({evaluation.email}).")
                self.unparsed_evaluations.add(evaluation)

        # signal the email daemon that all emails have been queued
        self._email_queue.put(EndOfStreamPacket())
        LOGGER.info("The EvaluateDaemon thread is finished.")


def _main() -> None:
    """Main function. (1) Asks the user for the name of a csv that contains applicant
    decisions. (2) Evaluates the applicants accordingly. (3) If there are any
    applicants whose decisions couldn't be parsed, create a new csv with only their
    information.
    """
    # get the csv filename from the user
    file_message = """
    Please input the name of the csv in inbox (e.g. evals.csv).
    Remember that this file MUST have email, first name, and
    decision columns. Of course, email must be a valid email
    address, and decision must be either accept, reject, or
    waitlist. These are all case sensitive.

    Filename: """
    filename = input(file_message)

    # make sure they actually want to do this
    followup_message = """
    Are you SURE that you want to do this? Running this script
    will update the applicants' profiles in the database and
    email them with their decisions. 
    
    Proceed? (y/n): """
    response = input(followup_message)
    if response != "y":
        return

    evaluated_users = read_evaluated_users(filename)

    message_queue = Queue()  # queue for the daemons to communicate
    consumer = EmailDaemon(message_queue)
    producer = EvaluateDaemon(evaluated_users, message_queue)

    # start the daemons
    consumer.start()
    producer.start()

    # wait for evaluations to finish
    producer.join()

    if producer.unparsed_evaluations:
        write_evaluations_to_csv("unparsed_evals", producer.unparsed_evaluations)

    # wait for emails to finish sending
    consumer.join()


if __name__ == "__main__":
    _main()
