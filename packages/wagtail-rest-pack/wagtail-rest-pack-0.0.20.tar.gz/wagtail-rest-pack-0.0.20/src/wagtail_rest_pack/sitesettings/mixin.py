from wagtail.admin.edit_handlers import InlinePanel
from wagtail.api import APIField

from wagtail_rest_pack.sitesettings.serializers import SiteSettingsSerializer
from django.utils.translation import gettext as _


class SiteSettingsPanelMixin:
    site_settings_panels = [
        InlinePanel('carouselitems', label=_('Carousel Items'))
    ]

    api_fields = [
        APIField('carouselitems', SiteSettingsSerializer())
    ]
