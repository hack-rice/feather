
from threading import Thread

from utils.quill_dao import QuillDao
from utils.data_packet import EmailPacket, EndOfStreamPacket


class EvaluateDaemon(Thread):
    def __init__(self, evaluations, email_queue):
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
                    EmailPacket("reject", evaluation.email, evaluation.first_name)
                )

            elif evaluation.decision == "accept":
                dao.reject_applicant(evaluation.email)

                self._email_queue.put(
                    EmailPacket("accept", evaluation.email, evaluation.first_name)
                )

            elif evaluation.decision == "waitlist":
                dao.waitlist_applicant(evaluation.email)

                self._email_queue.put(
                    EmailPacket("waitlist", evaluation.email, evaluation.first_name)
                )

            # --------------------
            # store unparsed evaluations
            # --------------------

            else:
                self.unparsed_evaluations.add(evaluation)

        # signal the email daemon that all emails have been queued
        self._email_queue.put(EndOfStreamPacket())
