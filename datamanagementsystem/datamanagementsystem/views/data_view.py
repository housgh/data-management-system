from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from ..serializers.data_serializer import DataSerializer, UpdateDataSerializer
from drf_yasg import openapi
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..helpers.schema_helper import get_tenant_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..services.data_service import DataService

skip = openapi.Parameter('skip', openapi.IN_QUERY,
                             description="skip number of records",
                             type=openapi.TYPE_INTEGER)

take = openapi.Parameter('take', openapi.IN_QUERY,
                             description="take number of records",
                             type=openapi.TYPE_INTEGER)

search_text = openapi.Parameter('search_text', openapi.IN_QUERY,
                             description="search by all property values",
                             type=openapi.TYPE_STRING)

data_service = DataService()


@swagger_auto_schema(manual_parameters=[skip, take, search_text], method='GET')
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_data(request, entity_id):
    skip = request.query_params.get('skip')
    take = request.query_params.get('take')
    search_text = request.query_params.get('search_text')
    schema = get_tenant_schema(request)
    data = data_service.get_all(schema, entity_id, skip, take, search_text)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_single(request, entity_id, id):
    schema = get_tenant_schema(request)
    data = data_service.get(schema, entity_id, id)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_single(request, entity_id, id):
    schema = get_tenant_schema(request)
    data_service.delete(schema, entity_id, id)
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_all(request, entity_id):
    schema = get_tenant_schema(request)
    data_service.delete_all(schema, entity_id)
    return Response(status=status.HTTP_200_OK)

@swagger_auto_schema(request_body=DataSerializer, method='POST')
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def insert_data(request, entity_id):
    body = DataSerializer(data=request.data)
    if body.is_valid():
        schema = get_tenant_schema(request)
        data_service.add(schema, entity_id, body.validated_data)
        return Response(body.validated_data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(request_body=UpdateDataSerializer, method='PUT')
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_data(request, entity_id, id):
    body = UpdateDataSerializer(data=request.data)
    if body.is_valid():
        schema = get_tenant_schema(request)
        data_service.update(schema, entity_id, id, body.validated_data)
        return Response(body.validated_data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)