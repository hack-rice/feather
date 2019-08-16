"""Script that evaluates applicants."""
from scripts.constants import Constants
from feather.email import GmailClient, JinjaEmailFactory
from feather import UnsubmittedUser


def _main() -> None:
    """Main function. (1) Asks the user for the name of a csv that contains applicant
    decisions. (2) Evaluates the applicants accordingly. (3) If there are any
    applicants whose decisions couldn't be parsed, create a new csv with only their
    information.
    """
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

    user = UnsubmittedUser("", "horeilly1101@gmail.com")
    users = [user for _ in range(250)]

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for user in users:
            client.send_mail(user.email, email)


if __name__ == "__main__":
    _main()
