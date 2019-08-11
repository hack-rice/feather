"""File that contains DataPacket classes. These objects comprise the API
for communicating with the email daemon.
"""


class DataPacket:
    pass


class EmailPacket(DataPacket):
    def __init__(self, template_name, email_subject, email, first_name):
        self.template_name = template_name
        self.email_subject = email_subject
        self.email = email
        self.first_name = first_name


class EndOfStreamPacket(DataPacket):
    pass
