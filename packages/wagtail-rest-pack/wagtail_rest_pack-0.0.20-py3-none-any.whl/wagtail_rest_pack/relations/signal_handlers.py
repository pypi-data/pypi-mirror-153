from django.db.models.signals import post_save, post_delete
from wagtail.core.models import Page
from .index import indexUpdated
from .index import indexDeleted


def on_page_saved(sender, *args, **kwargs):
    instance = kwargs.get('instance', None)
    if instance is not None and issubclass(sender, Page):
        indexUpdated(**kwargs)

def on_page_delete(sender, *args, **kwargs):
    instance = kwargs.get('instance', None)
    if instance is not None and issubclass(sender, Page):
        indexDeleted(**kwargs)

def register_signal_handlers():
    post_save.connect(on_page_saved)
    post_delete.connect(on_page_delete)

