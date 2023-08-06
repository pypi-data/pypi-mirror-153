from .response import FormResponse
from wagtail.core import blocks


class ShowSnackResponse(FormResponse):
    type='form_open_snack'

    @staticmethod
    def block_definition() ->tuple:
        return ShowSnackResponse.type, blocks.StructBlock(local_blocks=[
            ('text', blocks.TextBlock(required=True, max_length=50))
        ])
