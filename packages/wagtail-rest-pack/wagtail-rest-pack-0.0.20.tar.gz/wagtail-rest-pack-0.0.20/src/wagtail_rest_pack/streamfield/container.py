from rest_framework import serializers
from rest_framework.fields import empty
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from django.utils.translation import gettext_lazy as _

from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer


def container_block(local_blocks):
    return ContainerSerializer.block_definition(local_blocks=local_blocks)


class ContainerSerializer(serializers.Serializer):
    block_name = 'container'
    stream = SettingsStreamFieldSerializer()

    @staticmethod
    def block_definition(local_blocks):
        return ContainerSerializer.block_name, ContainerBlock(local_blocks=local_blocks, icon='doc-full', label=_('Column'))

    class Meta:
        fields = ('stream',)


class ContainerBlock(blocks.StructBlock):

    def __init__(self, local_blocks, *args, **kwargs):
        super().__init__(local_blocks=[
            ('stream', StreamBlock(empty=True, local_blocks=local_blocks, label=_('Content of Column'))),
        ], **kwargs)
