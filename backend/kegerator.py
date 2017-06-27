from kegpiapp.models import SettingsModel


class Kegerator:
    __state = {}

    def __init__(self):
        self.__dict__ = self.__state

        SettingsModel
