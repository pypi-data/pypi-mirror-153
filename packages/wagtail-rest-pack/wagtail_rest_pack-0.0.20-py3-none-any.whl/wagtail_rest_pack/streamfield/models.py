from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet


class GalleryImageBlock(blocks.StructBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(local_blocks=[
            ('id', ImageChooserBlock(icon='image', label=_('Image'))),
        ], **kwargs)


@register_snippet
class Gallery(ClusterableModel):
    name = models.CharField(max_length=120, help_text=_('Gallery name'))
    stream = StreamField(block_types=[
        ('gallery_image', GalleryImageBlock()),
    ])
    panels = [
        FieldPanel('name'),
        StreamFieldPanel('stream'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')
