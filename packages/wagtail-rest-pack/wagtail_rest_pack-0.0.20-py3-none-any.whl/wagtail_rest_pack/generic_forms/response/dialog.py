from .response import FormResponse
from wagtail.core import blocks
from django.utils.translation import gettext as _

class ShowDialogResponse(FormResponse):
    type= 'form_open_dialog'

    @staticmethod
    def block_definition() ->tuple:
        return ShowDialogResponse.type, blocks.StructBlock(local_blocks=[
            ('title', blocks.TextBlock(required=True, help_text=_('title'), max_length=40)),
            ('text', blocks.StreamBlock([
                ('richtext', blocks.RichTextBlock(icon="doc-full"))
            ]))
        ])
