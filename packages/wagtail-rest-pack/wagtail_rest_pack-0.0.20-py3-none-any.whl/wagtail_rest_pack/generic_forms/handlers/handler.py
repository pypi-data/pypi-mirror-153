from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer

from .email import EmailActionHandler

def get_handlers():
    return {
        'send_email': EmailActionHandler
    }

def handle(action, *args, **kwargs):
    value = action['value']
    assert len(value['action']) == 1, ('Only one action can be set.')
    assert len(value['response']) == 1, ('Only one response can be set.')
    response = value['response'][0]
    concrete_action = value['action'][0]
    handlers = get_handlers()
    handler = handlers.get(concrete_action['type'], None)
    assert handler is not None, ('No handler configured for %s' % concrete_action['type'])
    handler(**kwargs).handle(concrete_action['value'])
    return value['response']

