from rest_framework import serializers
from wagtail.core.blocks import RichTextBlock

from wagtail.core.templatetags.wagtailcore_tags import richtext as richtext_filter
from django.utils.translation import gettext as _



def rich_text(add_features: [str]):
    return RichTextSerializer.block_definition(add_features)


class RichTextSerializer(serializers.Serializer):
    block_name = 'richtext'
    text = serializers.SerializerMethodField('get_text')

    @staticmethod
    def block_definition(add_features: [str] = []):
        features = ['h2', 'h3', 'italic', 'bold', 'ol', 'ul', 'hr', 'link',
                    'document-link', 'image', 'embed', 'code',
                    'superscript', 'subscript', 'strikethrough', 'blockquote']
        features.extend(add_features)
        return RichTextSerializer.block_name, RichTextBlock(features=features,icon='doc-full')

    class Meta:
        fields = ('text',)

    def get_text(self, value):
        return richtext_filter(value.source)
