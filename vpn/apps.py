from django.apps import AppConfig


class VpnConfig(AppConfig):
    name = 'vpn'

    def ready(self):
        import vpn.signals  # noqa