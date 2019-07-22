"""File that contains the necessary functions to create and render an email."""
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from config import Config


def _render_template(filename, first_name):
    env = Environment(loader=FileSystemLoader(Config.TEMPLATES_PATH))
    template = env.get_template(filename)

    # render template with jinja2
    return template.render(first_name=first_name)


def create_email(applicant):
    mail = MIMEText(_render_template("accept.html", "Hugh"), "html")
    mail["Subject"] = "testing!"
    mail["From"] = Config.EMAIL
    mail["To"] = "horeilly1101@gmail.com"

    return mail