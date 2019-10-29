"""Script that updates applicants on reimbursement."""
from scripts.constants import Constants
from feather.email import GmailClient, JinjaEmailFactory
from feather.csv import CSVReader

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
                "reimbursements.html",
                reimbursement.email,
                first_name=reimbursement.first_name,
                address=reimbursement.address,
                amount=reimbursement.amount
            )

            client.send_mail(reimbursement.email, email)


if __name__ == "__main__":
    _main()
