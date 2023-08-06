from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomPageTagConfig(AppConfig):
    name = 'wagtail_rest_pack.custom_tag'
    verbose_name = _('Custom Page Tag')

    def ready(self):
        pass
