from wagtail.core import blocks

from wagtail_rest_pack.generic_forms.actions.action import FormAction
from django.utils.translation import gettext as _


class SendEmailAction(FormAction):
    type = 'send_email'

    @staticmethod
    def block_definition() -> tuple:
        return SendEmailAction.type, blocks.StructBlock(local_blocks=[
            ('sender', blocks.CharBlock(max_length=50, label=_('Technical name of a field containing a sender email address'))),
            ('address', blocks.EmailBlock(max_length=150, label=_('A email address to which a email should be delived to')))
        ])
