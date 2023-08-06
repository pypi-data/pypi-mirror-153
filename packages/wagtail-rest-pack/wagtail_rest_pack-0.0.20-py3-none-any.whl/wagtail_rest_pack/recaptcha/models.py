from django.conf import settings
from rest_framework.exceptions import ValidationError
from importlib import import_module

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class RecaptchaVerifier:

    def verify(self, request):
        pass


def get_recaptcha_instance() -> RecaptchaVerifier:
    class_str = getattr(settings, 'RECAPTCHA_VERIFIER', None)
    assert class_str is not None, ('Please, specify RECAPTCHA_VERIFIER in settings.')
    try:
        module_path, class_name = class_str.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)()
    except (ImportError, AttributeError) as e:
        raise ImportError(class_str)

