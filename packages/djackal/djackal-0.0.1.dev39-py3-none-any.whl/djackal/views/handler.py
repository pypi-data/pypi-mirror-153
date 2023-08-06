from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from djackal.exceptions import DjackalAPIException


def exception_handler(exc, context):
    if isinstance(exc, DjackalAPIException):
        return Response(exc.response_data(), status=exc.get_status_code())
    return drf_exception_handler(exc, context)
