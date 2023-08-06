import requests
from rest_framework.exceptions import ValidationError
from wagtail_rest_pack.recaptcha.models import RecaptchaVerifier
from django.conf import settings
from wagtail_rest_pack.recaptcha.models import get_client_ip
from django.utils.translation import gettext as _


class GoogleRecaptchaVerifier(RecaptchaVerifier):
    def verify(self, request):
        captcha_rs = request.data.get('g-recaptcha-response')
        if captcha_rs is None:
            raise ValidationError(_('Recaptcha field is empty'))
        url = "https://www.google.com/recaptcha/api/siteverify"
        ip = get_client_ip(request)
        secret = getattr(settings, 'GOOGLE_RECAPTCHA_SECRET', None)
        assert secret is not None, ('Please, define GOOGLE_RECAPTCHA_SECRET in settings.')
        params = {
            'secret': secret,
            'response': captcha_rs,
            'remoteip': "localhost" if ip == "127.0.0.1" else ip
        }
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        if not verify_rs.get("success", False):
            error = verify_rs.get('error-codes', None) or "Unspecified error."
            if isinstance(error, list):
                error = ",".join(error)
            raise ValidationError(_(f'Error while validating Recaptcha: {error}'), code="400")
