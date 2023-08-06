from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as CoreDjangoValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from wagtail.api.v2.utils import BadRequestError
from rest_framework import status

def custom_exception_handler(exc, context):
    if isinstance(exc, (BadRequestError,)):
        data = {'message': [str(exc)]}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exc, (ValidationError, CoreDjangoValidationError)):
        data = {'message': exc}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    return response