from rest_framework import serializers
from wagtail.core import blocks
from wagtail.core.blocks import StreamBlock
from django.utils.translation import gettext_lazy as _

from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer

from wagtail_rest_pack.streamfield.container import ContainerBlock, container_block


def containers_block(local_blocks):
    return ContainersSerializer.block_definition(local_blocks=local_blocks)


class ContainersSerializer(serializers.Serializer):
    block_name = 'containers'
    stream = SettingsStreamFieldSerializer()

    @staticmethod
    def block_definition(local_blocks):
        return ContainersSerializer.block_name, ContainersBlock(local_blocks=local_blocks, icon='container', label=_('More Columns'))

    class Meta:
        fields = ('stream',)


class ContainersBlock(blocks.StructBlock):

    def __init__(self, local_blocks, *args, **kwargs):
        super().__init__(local_blocks=[
            ('stream', StreamBlock(local_blocks=[
                container_block(local_blocks),
             ], label=_('Columns'))),
        ], **kwargs)
