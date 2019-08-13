from email.mime.text import MIMEText


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
