from builtins import super

from wagtail.core import blocks
from wagtail.embeds.embeds import get_embed
from rest_framework import serializers
from django.utils.translation import gettext as _

def embedded():
    return EmbeddedSerializer.block_definition()

embedded_variants = [
    ('signtranslate', _('Znakovaný překlad')),
    ('video', _('Obyčejné video')),
]
class EmbeddedSerializer(serializers.Serializer):
    block_name = 'embedded'
    definition = serializers.SerializerMethodField('create')

    @staticmethod
    def block_definition():
        return EmbeddedSerializer.block_name, CustomEmbeddedBlock(label=_('Embedded video'))

    def create(self, value):
        isSignTranslate = value['variant'] == 'signtranslate'
        autoplay = isSignTranslate
        useThumbnail = isSignTranslate

        embed = get_embed(value["url"])
        html = embed.html
        min_width = 400
        if embed.width < min_width:
            original_width = embed.width
            original_height = embed.height
            original_ratio = embed.ratio
            embed.width = min_width
            embed.height = int(min_width * original_ratio)
            html = html.replace('width="%s"' % original_width, 'width="300"')
            html = html.replace('height="%s"' % original_height, 'height="%s"' % embed.height)
        if autoplay:
            html = html.replace("feature=oembed", "feature=oembed&autoplay=1")
        return {
            'html': html,
            'thubmnail': embed.thumbnail_url,
            'width': embed.width,
            'height': embed.height,
            'title': embed.title,
            'useThumbnail': useThumbnail
        }

    class Meta:
        fields = ('definition')

class CustomEmbeddedBlock(blocks.StructBlock):
    url = blocks.CharBlock(help_text="Například https://www.youtube.com/watch&v=XqZsoesa55w")
    variant = blocks.ChoiceBlock(embedded_variants, label=_('Sign language translation'), default='signtranslate')

    def __init__(self, *args, **kwargs):
        super(CustomEmbeddedBlock, self).__init__(*args, **kwargs)

    class Meta:
        icon = "media"
