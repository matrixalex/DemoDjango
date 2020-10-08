from django.apps import AppConfig


class Config(AppConfig):
    name = 'src.apps.debts'
    label = 'debts'

    def ready(self):
        self.verbose_name = 'Долги'
