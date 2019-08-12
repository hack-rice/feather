"""File that contains DataPacket classes. These objects comprise the API
for communicating with the email daemon.
"""
from abc import ABC, abstractmethod


class DataPacket(ABC):
    def __init__(self, template_name: str, email_subject: str, email: str, first_name: str):
        self.template_name = template_name
        self.email_subject = email_subject
        self.email = email
        self.first_name = first_name

    @abstractmethod
    def stream_is_finished(self) -> bool:
        pass


class EmailPacket(DataPacket):
    def stream_is_finished(self) -> bool:
        return False


class EndOfStreamPacket(DataPacket):
    def __init__(self):
        super().__init__("", "", "", "")

    def stream_is_finished(self) -> bool:
        return True
