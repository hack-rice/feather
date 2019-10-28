from email.mime.text import MIMEText


class Email:
    """Class that represents an email. Can be rendered to an html string."""
    def __init__(self, email_subject: str, from_name: str, to_email: str, contents):
        self.email_subject = email_subject
        self.from_name = from_name
        self.to_email = to_email
        self.contents = contents

    def render(self) -> str:
        """Create and return a Mimetext email.
        :return: rendered Mimetext email
        """
        # for flexibility, we're allowing contents to be a string, or
        # a callable that returns a string
        try:
            contents = self.contents()
        except TypeError:
            contents = self.contents

        # render html and populate email headers
        mail = MIMEText(contents, "html")
        mail["Subject"] = self.email_subject
        mail["From"] = self.from_name
        mail["To"] = self.to_email

        return mail.as_string()
