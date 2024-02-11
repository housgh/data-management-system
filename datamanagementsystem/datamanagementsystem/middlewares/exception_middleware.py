import traceback
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from ..exceptions.missing_default_value_exception import MissingDefaultValueException


def ErrorResponse(status, data=None):
    response = Response(data,status=status)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response

class ExceptionMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        print(traceback.format_exc())
        if isinstance(exception, ObjectDoesNotExist):
           return ErrorResponse(status=status.HTTP_404_NOT_FOUND)
        if isinstance(exception , MissingDefaultValueException):
            return ErrorResponse(status=status.HTTP_400_BAD_REQUEST, data='equired properties require a default value.')
        return ErrorResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data='An Unexpected Error Has Occured.')
    
