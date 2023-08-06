from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.images import get_image_model_string
from wagtail.core.fields import RichTextField


@register_snippet
class ImageSliderItem(models.Model):
    image = models.ForeignKey(get_image_model_string(), on_delete=models.PROTECT, blank=False, null=True, default=None)
    text = RichTextField(features=['h2', 'h3', 'bold', 'italic', 'link'], max_length=200, blank=False, default="",
                         help_text="Text zobrazený přes obrázek.")

    panels = [
        FieldPanel('text'),
        ImageChooserPanel('image'),
    ]

    def __str__(self):
        return self.image.__str__() + " -> " + self.text

    class Meta:
        verbose_name = "Carousel Item"
        verbose_name_plural = "Carousel Items"
