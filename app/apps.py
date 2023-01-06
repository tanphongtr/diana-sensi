from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self) -> None:
        from . import signals
        return super().ready()