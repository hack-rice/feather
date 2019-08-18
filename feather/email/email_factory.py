"""File that contains the necessary functions to create and render an email."""
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
from feather.email.email import Email


class EmailFactory(ABC):
    @abstractmethod
    def create_email(self, *args, **kwargs) -> Email:
        pass


class JinjaEmailFactory(EmailFactory):
    def __init__(self, templates_directory_path, from_name: str):
        self.templates_directory_path = templates_directory_path
        self.from_name = from_name

    def _render_template(self, filename: str, first_name: str) -> str:
        # jinja2 boilerplate
        env = Environment(loader=FileSystemLoader(self.templates_directory_path))
        template = env.get_template(filename)

        # render template with jinja2
        return template.render(first_name=first_name)

    def create_email(self, email_subject: str, filename: str, first_name: str) -> Email:
        def contents():
            return self._render_template(filename, first_name)

        return Email(email_subject, self.from_name, contents)
