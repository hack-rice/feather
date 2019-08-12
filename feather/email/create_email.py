"""File that contains the necessary functions to create and render an email."""
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader


class EmailFactory:
    def __init__(self, templates_directory_path, from_email, from_name):
        self.templates_directory_path = templates_directory_path
        self.from_email = from_email
        self.from_name = from_name

    def _render_template(self, filename, first_name) -> str:
        """Render an email template.
        :return: html email string
        """
        # jinja2 boilerplate
        env = Environment(loader=FileSystemLoader(self.templates_directory_path))
        template = env.get_template(filename)

        # render template with jinja2
        return template.render(first_name=first_name)

    def create_email(self, filename, first_name, email_subject):
        def contents():
            return self._render_template(filename, first_name)

        return Email(
            contents,
            email_subject,
            self.from_name
        )


class Email:
    def __init__(self, contents, email_subject: str, from_name):
        self.contents = contents
        self.email_subject = email_subject
        self.from_name = from_name

    def render(self) -> str:
        """Create and return a Mimetext email.
        :return: configured Mimetext email
        """
        try:
            contents = self.contents()
        except TypeError:
            contents = self.contents

        # render html and populate email headers
        mail = MIMEText(contents, "html")
        mail["Subject"] = self.email_subject
        mail["From"] = self.from_name

        return mail.as_string()
