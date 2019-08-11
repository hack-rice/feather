"""File that contains DataPacket classes. These objects comprise the API
for communicating with the email daemon.
"""
from abc import ABC, abstractmethod
from typing import NamedTuple


class DataPacket(ABC, NamedTuple):
    template_name: str
    email_subject: str
    email: str
    first_name: str

    @abstractmethod
    def stream_is_finished(self) -> bool:
        pass


class EmailPacket(DataPacket):
    def stream_is_finished(self) -> bool:
        return False


class EndOfStreamPacket(DataPacket):
    def stream_is_finished(self) -> bool:
        return True
