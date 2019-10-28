"""Script that evaluates applicants."""
import logging

from scripts.constants import Constants
from feather.email import GmailClient, JinjaEmailFactory
from feather.csv import CSVReader

# Configure the logger
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

handler = logging.StreamHandler()

logger_format = logging.Formatter('%(levelname)s - %(name)s - %(asctime)s - %(message)s')
handler.setFormatter(logger_format)

LOGGER.addHandler(handler)

# configure the email subject for all of our emails
EMAIL_SUBJECT = f"{Constants.EVENT_NAME} Reimbursement Update"


def _main() -> None:
    """Main function."""
    # get the csv filename from the user
    file_message = """
        Please input the name of the csv in inbox (e.g. evals.csv).
        Remember that this file MUST have email, first name,
        amount, and address columns.

        Filename: """
    filename = input(file_message)

    reader = CSVReader(Constants.INBOX_PATH)
    reimbursements = reader.read_reimbursements(filename)

    email_factory = JinjaEmailFactory(Constants.TEMPLATES_PATH, f"The {Constants.EVENT_NAME} Team")

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for reimbursement in reimbursements:
            email = email_factory.create_email(
                EMAIL_SUBJECT,
                filename,
                reimbursement.email,
                first_name=reimbursement.first_name,
                address=reimbursement.address,
                amount=reimbursement.amount
            )

            client.send_mail(reimbursement.email, email)


if __name__ == "__main__":
    _main()
