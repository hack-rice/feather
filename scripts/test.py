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
    # retrieve users to email
    users = [
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com"),
        UnsubmittedUser("", "horeilly1101@gmail.com")
    ]
    fac = JinjaEmailFactory(Constants.TEMPLATES_PATH, Constants.EVENT_NAME)

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for user in users:
            email = fac.create_email("Hello!", "reminder.html", "My boy")
            client.send_mail(user.email, email)


if __name__ == "__main__":
    _main()
