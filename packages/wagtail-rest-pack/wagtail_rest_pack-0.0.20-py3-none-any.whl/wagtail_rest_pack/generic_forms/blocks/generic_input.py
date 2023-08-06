import re

from django.core.exceptions import ValidationError
from wagtail.core import blocks

from rest_framework import serializers
from wagtail_rest_pack.generic_forms.blocks.visibility import visibility_choices
from django.utils.translation import gettext_lazy as _


def is_form_field(value):
    if not isinstance(value, str):
        raise ValidationError(_('Only string type is allowed'))
    pattern = "^[a-zA-Z0-9_-]+$"
    pass
    if re.match(pattern, value) is None:
        raise ValidationError(_('Does not match a-z, A-Z'))

text_validation_choices = [
    ('none', _('None')),
    ('email', _('Email'))
]

class GenericInputBlock(blocks.StructBlock):
    def __init__(self, specific: [] = None, **kwargs):
        # todo validace na unikátnost name
        local_blocks = [
            ('name', blocks.TextBlock(max_length=30, help_text=_('The field name, e.g. email_field'),
                                      label=_('Technical name of a field'), validators=[is_form_field])),
            ('label', blocks.TextBlock(max_length=50, label=_('Label shown before input'))),
            ('max_length',
             blocks.IntegerBlock(label='Max', help_text=_('Max length of an input'), default=100, min_value=10,
                                 max_value=2000)),
            ('required', blocks.ChoiceBlock(choices=visibility_choices, default=visibility_choices[0][0], label=_('Condition of field visilibity'))),
            ('placeholder',
             blocks.CharBlock(max_length=80, required=False, help_text=_('Help text shown when nothing filled yet.'))),
            ('validation', blocks.ChoiceBlock(choices=text_validation_choices, default='none', label=_('Validation')))
        ]
        if specific is not None:
            local_blocks.extend(specific)
        super().__init__(local_blocks=local_blocks, **kwargs)

