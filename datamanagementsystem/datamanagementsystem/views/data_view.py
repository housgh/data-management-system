from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from ..serializers.data_serializer import DataSerializer
from ..helpers.sql_helper import get_records, get_record
from drf_yasg import openapi
from rest_framework.decorators import api_view
from ..helpers.schema_helper import get_tenant_schema

skip = openapi.Parameter('skip', openapi.IN_QUERY,
                             description="skip number of records",
                             type=openapi.TYPE_INTEGER)

take = openapi.Parameter('take', openapi.IN_QUERY,
                             description="take number of records",
                             type=openapi.TYPE_INTEGER)

search_text = openapi.Parameter('search_text', openapi.IN_QUERY,
                             description="search by all property values",
                             type=openapi.TYPE_STRING)


@swagger_auto_schema(manual_parameters=[skip, take, search_text], method='GET')
@api_view(['GET'])
def get_all_data(request, entity_name):
    skip = request.query_params.get('skip')
    take = request.query_params.get('take')
    search_text = request.query_params.get('search_text')
    schema = get_tenant_schema(request)
    data = get_records(schema, entity_name, skip, take, search_text)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_single(request, entity_name, id):
    schema = get_tenant_schema(request)
    data = get_record(schema, entity_name, id)
    return Response(data, status=status.HTTP_200_OK)