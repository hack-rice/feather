"""Script that evaluates applicants."""
import logging

from scripts.constants import Constants
from feather import QuillDao
from feather.email import GmailClient, JinjaEmailFactory
from feather.csv import CSVWriter, CSVReader

# Configure the logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()

logger_format = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')
handler.setFormatter(logger_format)

LOGGER.addHandler(handler)

# configure the email subject for all of our emails
EMAIL_SUBJECT = f"{Constants.EVENT_NAME} Application Decision"


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

    reader = CSVReader(Constants.INBOX_PATH)
    evaluations = reader.read_evaluated_users(filename)

    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    email_factory = JinjaEmailFactory(Constants.TEMPLATES_PATH, f"The {Constants.EVENT_NAME} Team")

    # keep track of evaluations that couldn't be parsed
    unparsed_evaluations = []

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for evaluation in evaluations:
            # --------------------
            # update database and queue email
            # --------------------

            if evaluation.decision == "Reject":
                dao.reject_applicant(evaluation.email)
                LOGGER.info(f"{evaluation.first_name}({evaluation.email}) has been rejected.")

                email = email_factory.create_email(EMAIL_SUBJECT, "reject.html", evaluation.first_name)
                client.send_mail(evaluation.email, email)

            if evaluation.decision == "Accept":
                dao.accept_applicant(evaluation.email)
                LOGGER.info(f"{evaluation.first_name}({evaluation.email}) has been accepted.")

                email = email_factory.create_email(EMAIL_SUBJECT, "accept.html", evaluation.first_name)
                client.send_mail(evaluation.email, email)

            elif evaluation.decision == "Waitlist":
                dao.waitlist_applicant(evaluation.email)
                LOGGER.info(f"{evaluation.first_name}({evaluation.email}) has been waitlisted.")

                email = email_factory.create_email(EMAIL_SUBJECT, "waitlist.html", evaluation.first_name)
                client.send_mail(evaluation.email, email)

            # --------------------
            # store unparsed evaluations
            # --------------------

            else:
                LOGGER.error(f"Unable to parse {evaluation.first_name}({evaluation.email}).")
                unparsed_evaluations.append(evaluation)

    if unparsed_evaluations:
        writer = CSVWriter(Constants.OUTBOX_PATH)
        writer.write_evaluations_to_csv("unparsed_evals", unparsed_evaluations)


if __name__ == "__main__":
    _main()
