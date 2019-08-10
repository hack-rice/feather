"""File that contains the EvaluateDaemon."""
from threading import Thread
from typing import Iterable
import logging

from feather.quill_dao import QuillDao
from feather.email.data_packet import EmailPacket, EndOfStreamPacket
from feather.models import Evaluation
from config import Config

LOGGER = logging.getLogger(__name__)

# configure the subject line for all the emails
EMAIL_SUBJECT = f"{Config.EVENT_NAME} Application Decision"


class EvaluateDaemon(Thread):
    """A daemon thread that evaluates hackathon applicants. See the run method
    for more details.
    """
    def __init__(self, evaluations: Iterable[Evaluation], email_queue: "Queue"):
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
