
from rest_framework import serializers, generics
from rest_framework.permissions import AllowAny
from wagtail.core.fields import StreamField
from wagtail_rest_pack.exception.handler import custom_exception_handler
from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer
from django.utils.translation import gettext_lazy as _

from .models import FormBuilder
from wagtail.snippets.blocks import SnippetChooserBlock


def form_block():
    return GetFormBuilderSerializer.block_definition()

class GetFormBuilderSerializer(serializers.ModelSerializer):
    block_name = 'form'
    stream = SettingsStreamFieldSerializer()

    @staticmethod
    def block_definition():
        return GetFormBuilderSerializer.block_name, SnippetChooserBlock(target_model='generic_forms.FormBuilder', label=_('form'), icon='form')

    class Meta:
        model = FormBuilder
        fields = ['name', 'display_name', 'description', 'security', 'stream']

