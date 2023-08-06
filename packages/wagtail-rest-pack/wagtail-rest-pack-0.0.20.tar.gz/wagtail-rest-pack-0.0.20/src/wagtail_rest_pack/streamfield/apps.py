from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class StreamfieldConfig(AppConfig):
    name = 'wagtail_rest_pack.streamfield'
    verbose_name = _('StreamField Additions')

    def ready(self):
        pass
        # super().ready()