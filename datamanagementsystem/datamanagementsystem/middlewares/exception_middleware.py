import traceback
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status


class ExceptionMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            response = self.get_response(request)
        except ObjectDoesNotExist:
            raise Http404
        except Exception:
            print(traceback.format_exc())
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response