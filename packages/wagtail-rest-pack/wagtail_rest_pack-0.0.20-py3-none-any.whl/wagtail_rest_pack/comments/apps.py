from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CommentsConfig(AppConfig):
    name = 'wagtail_rest_pack.comments'
    verbose_name = _('Comments')

    def ready(self):
        pass