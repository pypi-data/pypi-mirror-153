
from rest_framework import serializers
from wagtail.core import blocks
from django.utils.translation import gettext_lazy as _
from wagtail.core.blocks import StreamBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail_rest_pack.streamfield.models import Gallery

from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer, get_stream_field_serializers



def gallery_block():
    return GallerySerializer.block_definition()


class GallerySerializer(serializers.ModelSerializer):
    block_name = 'gallery'
    images = serializers.SerializerMethodField('get_images')

    @staticmethod
    def block_definition():
        return GallerySerializer.block_name, SnippetChooserBlock(target_model=Gallery, label=_('Gallery'), icon='image')

    class Meta:
        model = Gallery
        fields = ['name', 'images', ]

    def get_images(self, gallery):
        data = gallery.stream.raw_data
        serializers = get_stream_field_serializers()
        for item in data:
            cls = serializers.get(item['type'])
            assert cls is not None, (
                '%s serializers is not registered.' % item['type']
            )
            yield cls(item['value']).data

