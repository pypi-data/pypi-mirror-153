from django.conf import settings
from rest_framework import serializers
from wagtail.core import blocks
from django.utils.translation import gettext_lazy as _
from wagtail.core.blocks import StreamBlock

from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer

rest_pack = getattr(settings, "REST_PACK", {})
icons = rest_pack.get('icons', [])


class LinkCategorySerializer(serializers.Serializer):
    block_name = 'linkcategory'

    name = serializers.CharField(max_length=50)
    icon = serializers.CharField()
    stream = SettingsStreamFieldSerializer()

    @staticmethod
    def block_definition(local_blocks):
        return LinkCategorySerializer.block_name, blocks.StructBlock(local_blocks=[
            ('name', blocks.TextBlock(max_length=50, required=True, help_text=_('Name of the category'))),
            ('stream', StreamBlock(local_blocks, label=_('A nested content of a category'))),
            ('icon', blocks.ChoiceBlock(choices=[('none', _('None'))] + icons, default=['none'], label=_('The icon'))),
        ])

    class Meta:
        fields = ['name', 'stream', 'icon']


class LinkBlockSerializer(serializers.Serializer):
    block_name = 'linkblock'

    name = serializers.CharField(max_length=50)
    icon = serializers.CharField()
    page = serializers.SerializerMethodField('get_page_repre')

    @staticmethod
    def block_definition(nested:bool=False):
        local_block_name = LinkBlockSerializer.block_name
        if nested:
            local_block_name = 'nested'+local_block_name
        return local_block_name, blocks.StructBlock(local_blocks=[
            ('name', blocks.TextBlock(max_length=50, required=True, help_text=_('Name of the link'))),
            ('page', blocks.PageChooserBlock(label=_('A page to be opened'))),
            ('icon', blocks.ChoiceBlock(choices=[('none', _('None'))] + icons, default=['none'], label=_('The icon'))),
        ])

    def get_page_repre(self, value):
        page = value['page']
        return {
            'id': page.id,
            'url': page.url,
        }

    class Meta:
        fields = ['name', 'page', 'icon']



class ChildrenLinksSerializer(serializers.Serializer):
    block_name = 'categorychildren'
    children = serializers.SerializerMethodField('get_page_repre')

    @staticmethod
    def block_definition():
        return ChildrenLinksSerializer.block_name, blocks.StructBlock(local_blocks=[
            ('parent', blocks.PageChooserBlock(label=_('A page which children should be listed'))),
        ])

    def get_page_repre(self, value):
        parent = value['parent']
        children_qs = parent.specific.children
        # todo limit somehow, or filter according to "show_in_menus"
        children = map(lambda child: {'name': child.title, 'page': child, 'icon':''}, children_qs)
        return LinkBlockSerializer(instance=children, many=True).data

    class Meta:
          fields = ['children',]