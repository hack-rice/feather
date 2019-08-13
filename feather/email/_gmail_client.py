import smtplib
import ssl


class GmailClient:
    def __init__(self, username, password):
        self._username = username
        self._password = password

        # store a connection to the server, initialize lazily
        self._server = None

    def _get_server_connection(self):
        # create and secure server connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls(context=ssl.create_default_context())

        # log in to your email
        server.login(self._username, self._password)
        return server


