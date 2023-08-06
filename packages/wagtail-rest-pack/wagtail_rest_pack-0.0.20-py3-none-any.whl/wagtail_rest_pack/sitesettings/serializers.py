from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField
from django.conf import settings

class SiteSettingsSerializer(Field):
    """A custom serializer used in Wagtails v2 API."""

    def get_single(self, obj):
        desktop_renderition = getattr(settings, 'IMAGE_LARGE_RENDERITION', 'width-1280')
        mobile_renderition = getattr(settings, 'IMAGE_SMALL_RENDERITION', 'width-480')
        return {
            'large': ImageRenditionField(desktop_renderition).to_representation(obj.image),
            'small': ImageRenditionField(mobile_renderition).to_representation(obj.image),
            'text': obj.text
        }

    def parse_sliders(self, page):
        return [self.get_single(setting.slider) for setting in page.carouselitems.all()]

    def get_sliders_of(self, page):
        if page is None:
            return []
        sliders = self.parse_sliders(page)
        if page.depth == 1:
            return sliders
        if len(sliders) == 0:
            return self.get_sliders_of(page.get_parent().specific)
        return sliders

    def to_representation(self, value):
        sliders = self.get_sliders_of(value.instance)
        return {
            "sliders": sliders
        }