
class DataPacket:
    pass


class EmailPacket(DataPacket):
    def __init__(self, template_name, email, first_name=None):
        self.template_name = template_name
        self.email = email
        self._first_name = first_name

    @property
    def first_name(self) -> str:
        if self._first_name:
            return self._first_name

        return "Hacker"


class EndOfStreamPacket(DataPacket):
    pass
