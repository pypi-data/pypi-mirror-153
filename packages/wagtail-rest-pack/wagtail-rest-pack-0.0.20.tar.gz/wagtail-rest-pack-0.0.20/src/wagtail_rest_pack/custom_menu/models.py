from django.utils.translation import gettext_lazy as _
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from django.conf import settings
from django.db import models
from wagtail_rest_pack.custom_menu.serializers import LinkBlockSerializer
from wagtail_rest_pack.streamfield.containers import ContainersSerializer
from wagtail_rest_pack.custom_menu.serializers import LinkCategorySerializer
from wagtail_rest_pack.custom_menu.serializers import ChildrenLinksSerializer

default_names = [('default', 'default')]
choices = getattr(settings, "REST_PACK", {}).get('custom_menu', {'names': default_names}).get('names', default_names)

@register_snippet
class CustomMenu(models.Model):

    name = models.CharField(max_length=50, choices=choices, primary_key=True)
    stream = StreamField(block_types=[
        ContainersSerializer.block_definition([
            LinkBlockSerializer.block_definition(nested=True),
            LinkCategorySerializer.block_definition([
                LinkBlockSerializer.block_definition(nested=True),
                ChildrenLinksSerializer.block_definition(),
            ])
        ]),
        LinkBlockSerializer.block_definition(),
        LinkCategorySerializer.block_definition([
            LinkBlockSerializer.block_definition(nested=True),
            ChildrenLinksSerializer.block_definition(),
        ])
    ], default=[])

    def __str__(self):
        return str(dict((x, y) for x, y in choices)[self.name])

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
