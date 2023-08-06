from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from wagtail.core import blocks
from wagtail_rest_pack.generic_forms.blocks.generic_input import GenericInputBlock, visibility_choices, text_validation_choices

from django.utils.translation import gettext_lazy as _


class InputBlockSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    label = serializers.CharField(max_length=50)
    max_length = serializers.IntegerField(max_value=2000, min_value=10)
    required = serializers.ChoiceField(choices=visibility_choices)
    placeholder = serializers.CharField(max_length=80, required=False)
    validation = serializers.ChoiceField(choices=text_validation_choices)
    multiline = serializers.BooleanField()

    block_name = 'form_text'

    @staticmethod
    def block_definition():
        return InputBlockSerializer.block_name, GenericInputBlock(specific=[
            ('multiline', blocks.BooleanBlock(required=False, help_text="Víceřádkový vstup."))
        ])

    class Meta:
        fields = ('name','label','max_length','required','placeholder','validation','multiline',)

    def validate_field(self, attr):
        instance = self.context['instance']
        field_name = instance['name']
        value = attr.get(field_name, None)
        if not isinstance(value, str):
            raise ValidationError(_(f'Expected "{field_name}" to be string, but is not'))
        if instance['required'] == 'anonymous_user_only':
            if self.context['request'].user.is_authenticated:
                if value is not None:
                    raise ValidationError(_(f'Expected "{field_name}" to be not set, but it is.'))
                return {}

        if value is None:
            raise ValidationError(_(f'Expected "{field_name}" to be set, but is not'))

        max_length = instance['max_length']
        if len(value) > max_length:
            raise ValidationError(_(f'Expected "{field_name}" to be of max_length "{max_length}"'))
        if instance['validation'] == "email":
            validate_email(value)
        return {
            field_name: value
        }
