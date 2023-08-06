from wagtail.admin.edit_handlers import InlinePanel
from wagtail.api import APIField
from wagtail_rest_pack.page_banner.serializers import BanneredChildrenSerializer
from wagtail_rest_pack.relations.models import Relation

from wagtail_rest_pack.sitesettings.serializers import SiteSettingsSerializer
from django.utils.translation import gettext as _
from wagtail.core.models import Page


class RelationsMixin:
    api_fields = [
        APIField('relations', serializer=BanneredChildrenSerializer())
    ]

    @property
    def relations(self):
        return Page.objects.filter(id__in=Relation.objects.filter(to_page_id=self.id).values('from_page_id'))
