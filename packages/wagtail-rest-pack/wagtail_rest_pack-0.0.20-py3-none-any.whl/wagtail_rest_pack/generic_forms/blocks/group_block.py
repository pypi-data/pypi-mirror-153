from rest_framework import serializers
from wagtail.core import blocks
from wagtail_rest_pack.generic_forms.blocks.text_block import InputBlockSerializer
from wagtail_rest_pack.generic_forms.blocks.visibility import visibility_choices
from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer
from django.utils.translation import gettext_lazy as _


class GroupBlockSerializer(serializers.Serializer):
    block_name = 'form_group'
    name = serializers.CharField(max_length=80)
    row = serializers.BooleanField()
    required = serializers.ChoiceField(choices=visibility_choices)
    stream = SettingsStreamFieldSerializer()
    class Meta:
        fields = ('name', 'row', 'required', 'stream',)

    @staticmethod
    def block_definition():
        return GroupBlockSerializer.block_name, GroupBlock(stream_blocks=[
            InputBlockSerializer.block_definition()
        ])

    def validate(self, attrs):
        pass

class GroupBlock(blocks.StructBlock):

    def __init__(self, stream_blocks, **kwargs):
        self.stream_definition = blocks.StreamBlock(local_blocks=stream_blocks)
        local_blocks = [
            ('name', blocks.CharBlock(max_length=80)),
            ('row', blocks.BooleanBlock(required=False, default=False, label=_('Show on a single line'))),
            ('required', blocks.ChoiceBlock(choices=visibility_choices, default=visibility_choices[0][0], label=_('Condition of visibility'))),
            ('stream', self.stream_definition)
        ]
        super().__init__(local_blocks=local_blocks, **kwargs)

