from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomMenuConfig(AppConfig):
    name = 'wagtail_rest_pack.custom_menu'
    verbose_name = _('Custom Page Menu')

    def ready(self):
        pass
