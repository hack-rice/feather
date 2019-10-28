"""File that contains the necessary functions to create and render an email."""
from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
from feather.email.email import Email


class EmailFactory(ABC):
    """
    An email factory interface. If you need to create emails in a new
    way, or with a new format, extend this class.
    """
    @abstractmethod
    def create_email(self, *args, **kwargs) -> Email:
        """
        Create an Email.
        :return: Email.
        """
        pass


class JinjaEmailFactory(EmailFactory):
    """
    Email factory that renders email contents with Jinja 2.
    """
    def __init__(self, templates_directory_path, from_name: str):
        """
        :param templates_directory_path: the path to the templates directory.
            You should use os.path to get this information.
        :param from_name: the name of who the email is from. This is what the
            receiver will see in their inbox.
        """
        self.templates_directory_path = templates_directory_path
        self.from_name = from_name

    def _render_template(self, filename: str, **template_variables) -> str:
        """
        Render the specified jinja2 template with the given template variables.

        :param filename: the filename of the template to be rendered. (e.g.
            "accept.html")
        :param template_variables: the variables that will be available in the
            jinja2 template. For example, including the variable first_name will
            allow you to access a user's first name in the template with
            {{ first_name }}.
        :return: rendered template, as a string
        """
        # jinja2 boilerplate
        env = Environment(loader=FileSystemLoader(self.templates_directory_path))
        template = env.get_template(filename)

        # render template with jinja2
        return template.render(**template_variables)

    def create_email(
            self,
            email_subject: str,
            filename: str,
            to_email: str,
            **template_variables
    ) -> Email:
        """
        :param email_subject: the subject of the email. This is what a receiver
            will see in their inbox.
        :param filename: the filename of the template to be rendered. (e.g.
            "accept.html")
        :param to_email: the email address you want to send the email to.
        :param template_variables: the variables that will be available in the
            jinja2 template. For example, including the variable first_name will
            allow you to access a user's first name in the template with
            {{ first_name }}.
        :return: an Email object.
        """
        def contents():
            return self._render_template(filename, **template_variables)

        return Email(email_subject, self.from_name, to_email, contents)
