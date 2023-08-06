from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StreamfieldConfig(AppConfig):
    name = 'wagtail_rest_pack.relations'
    verbose_name = _('Relations Additions')

    def ready(self):
        from .signal_handlers import register_signal_handlers
        register_signal_handlers()
