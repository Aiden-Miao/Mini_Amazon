from django.apps import AppConfig


class AmazonwebConfig(AppConfig):
    name = 'amazonweb'

    def ready(self):
        import amazonweb.signals

