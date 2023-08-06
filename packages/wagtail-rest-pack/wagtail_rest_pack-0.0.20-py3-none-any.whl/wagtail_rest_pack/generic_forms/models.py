from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail_rest_pack.generic_forms.blocks.group_block import GroupBlockSerializer
from wagtail_rest_pack.generic_forms.blocks.submit_block import SubmitBlockSerializer
from wagtail_rest_pack.generic_forms.blocks.text_block import InputBlockSerializer
from wagtail_rest_pack.recaptcha.permission import AuthenticatedOrRecaptcha
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext as _
from wagtailmodelchooser import register_simple_model_chooser

security_choices = {
    'recaptcha_or_user': {
        'label': _('Recaptcha or logged user'),
        'permission_classes': [AuthenticatedOrRecaptcha]
    },

    'authenticated_user_only': {
        'label': _('Authenticated user only'),
        'permission_classes': [IsAuthenticated]
    }
}


@register_snippet
@register_simple_model_chooser
class FormBuilder(ClusterableModel):
    name = models.CharField(max_length=60, validators=[], primary_key=True)
    display_name = models.TextField(max_length=100, default="")
    description = models.TextField(max_length=1000, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    security = models.CharField(max_length=30, default=next(iter(security_choices.items()))[0],
                                choices=[(choice[0],choice[1]['label']) for choice in security_choices.items()])
    stream = StreamField(block_types=[
        InputBlockSerializer.block_definition(),
        GroupBlockSerializer.block_definition(),
        SubmitBlockSerializer.block_definition(),
    ])

    def find_action(self, action):
        submittables = [action for action in self.stream.raw_data if action['type'] == 'form_submit']
        candidates = [candidate for candidate in submittables if candidate['value']['name'] == action]
        if len(candidates) != 1:
            return None
        return candidates[0]

    def __str__(self):
        return 'Formulář "{}"'.format(self.display_name)
