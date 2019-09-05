
from feather import QuillDao
from scripts.constants import Constants
from feather.email import JinjaEmailFactory, GmailClient


def _main() -> None:
    """Main function."""
    # retrieve users to email
    dao = QuillDao(Constants.MONGODB_URI, Constants.DB_NAME)
    confirmed_users = dao.get_confirmed_users()

    email_factory = JinjaEmailFactory(
        templates_directory_path=Constants.TEMPLATES_PATH,
        from_name=f"The {Constants.EVENT_NAME} Team"
    )

    with GmailClient(Constants.EMAIL, Constants.EMAIL_PASSWORD) as client:
        for user in confirmed_users:
            email = email_factory.create_email(
                email_subject="HackRice 9 Event Details",
                filename="confirm.html",
                first_name=user.first_name,
                to_email=user.email
            )
            client.send_mail(user.email, email)


if __name__ == "__main__":
    _main()
