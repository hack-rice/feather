"""File that contains the User model class."""


class _JsonDecoder:
    def __init__(self, json_obj):
        self._json_obj = json_obj

    def get_or_none(self, *args):
        result = None
        for arg in args:
            try

class User:
    def __init__(self, user_json):
        self._user_json = user_json

    @property
    def name(self):
        return
