from django.conf import settings
from django.http import HttpResponse

class VersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.version = getattr(settings, 'APPLICATION_VERSION', None)
        assert self.version is not None, (
            'The `APPLICATION_VERSION` must be set in order to use VersionMiddleware.'
        )

    def __call__(self, request):
        accept_version = request.headers.get('if-version')
        if accept_version is not None:
            if accept_version != self.version:
                response = self.get_response(request)
                return HttpResponse(status=412)
        response = self.get_response(request)
        response["Version"] = self.version
        return response
