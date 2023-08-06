from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    name = 'allianceauth.analytics'
    label = 'analytics'

    def ready(self):
        import allianceauth.analytics.signals
