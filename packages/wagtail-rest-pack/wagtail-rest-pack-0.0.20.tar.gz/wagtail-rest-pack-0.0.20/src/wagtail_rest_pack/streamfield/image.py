from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from wagtail.images import get_image_model
from rest_framework.fields import Field
from wagtail.images.api.fields import ImageRenditionField
from django.conf import settings


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('create_image')

    class Meta:
        model = get_image_model()
        fields = ['image',]

    def create_image(self, data):
        model = get_image_model()
        image = model.objects.get(id=data['id'])
        large_renderition = getattr(settings, 'IMAGE_LARGE_RENDERITION', 'width-1280')
        small_renderition = getattr(settings, 'IMAGE_BANNER_RENDERITION', 'fill-300x200')
        return {
            'id': data['id'],
            'title': image.title,
            'caption': image.caption,
            'large': ImageRenditionField(large_renderition).to_representation(image),
            'small': ImageRenditionField(small_renderition).to_representation(image),
        }


