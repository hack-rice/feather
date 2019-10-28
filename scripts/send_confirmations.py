
from feather import QuillDao, Applicant
from scripts.constants import Constants
from feather.email import JinjaEmailFactory, GmailClient


def _main() -> None:
    """Main function."""
    # retrieve users to email
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    confirmed_users = dao.get_confirmed_users()
    # confirmed_users = [Applicant("hjo2@rice.edu", "Hugh", None, None)]

    email_factory = JinjaEmailFactory(
        templates_directory_path=Constants.TEMPLATES_PATH,
        from_name=f"The {Constants.EVENT_NAME} Team"
    )

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for user in confirmed_users:
            email = email_factory.create_email(
                email_subject="HackRice: A Message from our Sponsors",
                filename="confirm.html",
                to_email=user.email,
                first_name=user.first_name
            )
            client.send_mail(user.email, email)


if __name__ == "__main__":
    _main()
