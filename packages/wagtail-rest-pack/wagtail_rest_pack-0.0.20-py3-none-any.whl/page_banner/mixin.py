from wagtail.api import APIField
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images import get_image_model_string
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.images.api.fields import ImageRenditionField
from django.conf import settings


class PageBannerMixin(models.Model):
    banner_title = models.TextField(max_length=100, blank=False, default="")
    banner_subtitle = models.TextField(max_length=500, blank=False, default="")
    banner_image = models.ForeignKey(get_image_model_string(), on_delete=models.PROTECT, blank=False, null=True,
                                     default=None)

    page_banner_panels = [
        MultiFieldPanel(
            heading="Page Banner",
            children=[
                FieldPanel('banner_title'),
                FieldPanel('banner_subtitle'),
                ImageChooserPanel('banner_image'),
            ]
        ),
    ]

    api_fields = [
        APIField('banner_title'),
        APIField('banner_subtitle'),
        APIField('banner_image',
                 serializer=ImageRenditionField(getattr(settings, 'IMAGE_BANNER_RENDERITION', 'fill-300x200'))),
    ]

    class Meta:
        abstract = True
