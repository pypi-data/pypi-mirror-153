from wagtail_rest_pack.recaptcha.models import RecaptchaVerifier


class NoopRecaptchaVerifier(RecaptchaVerifier):
    def verify(self, request):
        pass