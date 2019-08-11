"""File that contains the necessary functions to create and render an email."""
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from constants import Constants


def _render_template(filename: str, first_name: str) -> str:
    """Render an email template.

    :param filename: the filename of the email template. This file MUST be located
        in the configured templates directory.
    :param first_name: the first name of the applicant
    :return: html email string
    """
    # jinja2 boilerplate
    env = Environment(loader=FileSystemLoader(Constants.TEMPLATES_PATH))
    template = env.get_template(filename)

    # render template with jinja2
    return template.render(first_name=first_name)


def create_email(filename: str, email_subject: str, to_email: str, first_name: str) -> MIMEText:
    """
    Create and return a Mimetext email.

    :param filename: the filename of the email template. This file MUST be located
        in the configured templates directory.
    :param email_subject: the subject of the email, as it will be displayed in the
        receiver's inbox
    :param to_email: the email address the email will be sent to
    :param first_name: the first name of the email receiver
    :return: configured Mimetext email
    """
    # render html and populate email headers
    mail = MIMEText(_render_template(filename, first_name), "html")
    mail["Subject"] = email_subject
    mail["From"] = Constants.EMAIL
    mail["To"] = to_email

    return mail
