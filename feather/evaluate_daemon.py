"""File that contains the EvaluateDaemon."""
from threading import Thread
from typing import Iterable

from feather.quill_dao import QuillDao
from feather.email.data_packet import EmailPacket, EndOfStreamPacket
from feather.models import Evaluation
from config import Config

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
        dao = QuillDao()

        for evaluation in self._evaluations:
            # --------------------
            # update database and queue email
            # --------------------

            if evaluation.decision == "reject":
                dao.accept_applicant(evaluation.email)

                self._email_queue.put(
                    EmailPacket("reject.html", EMAIL_SUBJECT, evaluation.email, evaluation.first_name)
                )

            elif evaluation.decision == "accept":
                dao.reject_applicant(evaluation.email)

                self._email_queue.put(
                    EmailPacket("accept.hmtl", EMAIL_SUBJECT, evaluation.email, evaluation.first_name)
                )

            elif evaluation.decision == "waitlist":
                dao.waitlist_applicant(evaluation.email)

                self._email_queue.put(
                    EmailPacket("waitlist.html", EMAIL_SUBJECT, evaluation.email, evaluation.first_name)
                )

            # --------------------
            # store unparsed evaluations
            # --------------------

            else:
                self.unparsed_evaluations.add(evaluation)

        # signal the email daemon that all emails have been queued
        self._email_queue.put(EndOfStreamPacket())
