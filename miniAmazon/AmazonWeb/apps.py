from django.apps import AppConfig


class AmazonwebConfig(AppConfig):
    name = 'AmazonWeb'

    def ready(self):
    	import AmazonWeb.signals
