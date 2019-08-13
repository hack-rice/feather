"""Script that evaluates applicants."""
from scripts.constants import Constants
from feather.email import GmailClient, JinjaEmailFactory
from feather import QuillDao


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

    # retrieve users to email
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    unsubmitted_users = dao.get_unsubmitted_users()

    email_factory = JinjaEmailFactory(
        templates_directory_path=Constants.TEMPLATES_PATH,
        from_name=f"The {Constants.EVENT_NAME} Team"
    )

    # we want to send everyone the same email
    email = email_factory.create_email(
        email_subject="HackRice 9 Application Deadline",
        filename="reminder.html",
        first_name="Hacker"
    )

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for user in unsubmitted_users:
            client.send_mail(user.email, email)


if __name__ == "__main__":
    _main()
