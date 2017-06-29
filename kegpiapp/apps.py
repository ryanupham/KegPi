from django.apps import AppConfig


class KegpiappConfig(AppConfig):
    name = 'kegpiapp'

    def ready(self):
        import backend.sensors
