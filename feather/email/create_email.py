"""File that contains the necessary functions to create and render an email."""
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from config import Config


def _render_template(filename, first_name):
    env = Environment(loader=FileSystemLoader(Config.TEMPLATES_PATH))
    template = env.get_template(filename)

    # render template with jinja2
    return template.render(first_name=first_name)


def create_email(filename, email_subject, to_email, first_name):
    # render html and populate email headers
    mail = MIMEText(_render_template(filename, first_name), "html")
    mail["Subject"] = email_subject
    mail["From"] = Config.EMAIL
    mail["To"] = to_email

    return mail
