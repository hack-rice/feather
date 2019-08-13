"""File that contains DataPacket classes. These objects comprise the API
for communicating with the email daemon.
"""
from abc import ABC, abstractmethod
from feather.email.email import Email


class DataPacket(ABC):
    def __init__(self, to_email: str, email: Email):
        self.to_email = to_email
        self.email = email

    @abstractmethod
    def stream_is_finished(self) -> bool:
        pass


class EmailPacket(DataPacket):
    def stream_is_finished(self) -> bool:
        return False


class EndOfStreamPacket(DataPacket):
    def __init__(self):
        dummy_email = Email("", "", "")
        super().__init__("", dummy_email)

    def stream_is_finished(self) -> bool:
        return True
