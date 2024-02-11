from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from ..serializers.data_serializer import DataSerializer, UpdateDataSerializer
from ..helpers.sql_helper import get_records, get_record, insert_records, delete_record, delete_all_records, update_record
from drf_yasg import openapi
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..helpers.schema_helper import get_tenant_schema
from ..models.entity import Entity
from ..models.property import Property
from rest_framework_simplejwt.authentication import JWTAuthentication

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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_data(request, entity_id):
    skip = request.query_params.get('skip')
    take = request.query_params.get('take')
    search_text = request.query_params.get('search_text')
    schema = get_tenant_schema(request)
    entity = Entity.objects.get(pk=entity_id)
    data = get_records(schema, entity.entity_name, skip, take, search_text)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_single(request, entity_id, id):
    schema = get_tenant_schema(request)
    entity = Entity.objects.get(pk=entity_id)
    data = get_record(schema, entity.entity_name, id)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_single(request, entity_id, id):
    schema = get_tenant_schema(request)
    entity = Entity.objects.get(pk=entity_id)
    data = delete_record(schema, entity.entity_name, id)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_all(request, entity_id):
    schema = get_tenant_schema(request)
    entity = Entity.objects.get(pk=entity_id)
    data = delete_all_records(schema, entity.entity_name)
    return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(request_body=DataSerializer, method='POST')
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def insert_data(request, entity_id):
    body = DataSerializer(data=request.data)
    if body.is_valid():
        schema = get_tenant_schema(request)
        entity = Entity.objects.get(pk=entity_id)
        records = body.validated_data['records']
        data = []
        for dictionary in records:
            properties = Property.objects.filter(id__in=dictionary.keys()).all()
            data.append(dict([(property.property_name, dictionary[str(property.pk)]) for property in properties]))
        insert_records(schema, entity.entity_name, data)
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
        entity = Entity.objects.get(pk=entity_id)
        record = body.validated_data['record']
        properties = Property.objects.filter(id__in=record.keys()).all()
        data = dict([(property.property_name, record[str(property.pk)]) for property in properties])
        update_record(schema, entity.entity_name, id, data)
        return Response(body.validated_data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)