from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..helpers.sql_helper import update_column_name, add_column, update_column_type, remove_column
from ..serializers.property_serializer import (
    PropertySerializer, 
    UpdatePropertyNameSerializer, 
    DeletePropertySerializer, 
    UpdatePropertyTypeSerializer)
from ..helpers.schema_helper import get_tenant_schema
from rest_framework.decorators import action
from ..models.entity import Entity
from ..models.property import Property
from rest_framework.permissions import IsAuthenticated


class PropertyAPIView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PropertySerializer)
    @action(detail=False, methods=['post'])
    def post(self, request):
        entity_property = PropertySerializer(data=request.data)
        schema = get_tenant_schema(request)
        if(entity_property.is_valid()):
            data = entity_property.validated_data
            if(data['required'] and data.get('default_value') is None):
                return Response('Required properties require a default value.', status=status.HTTP_400_BAD_REQUEST)
            entity = Entity.objects.get(pk=entity_property.validated_data['entity_id'])
            add_column(schema, entity.entity_name, data)
            entity_property.save()
            return Response(entity_property.validated_data, status=status.HTTP_201_CREATED)
        return Response(entity_property.validated_datas, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=UpdatePropertyNameSerializer)
    @action(detail=False, methods=['put'])
    def update_name(self, request):
        update_property_name_model = UpdatePropertyNameSerializer(data=request.data)
        schema = get_tenant_schema(request)
        if(update_property_name_model.is_valid()):
            data = update_property_name_model.validated_data
            entity = Entity.objects.get(pk=data['entity_id'])
            db_property = Property.objects.get(pk=data['property_id'])
            update_column_name(schema, entity.entity_name, db_property.property_name, data['new_property_name'])
            db_property.property_name = data['new_property_name']
            db_property.save()
            return Response(None, status=status.HTTP_200_OK)
        return Response(update_property_name_model.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UpdatePropertyTypeSerializer)
    @action(detail=False, methods=['put'])
    def update_type(self, request):
        update_property_type_model = UpdatePropertyTypeSerializer(data=request.data)
        schema = get_tenant_schema(request)
        if(update_property_type_model.is_valid()):
            data = update_property_type_model.validated_data
            if(data['required'] and data.get('default_value') is None):
                return Response('Required properties require a default value.', status=status.HTTP_400_BAD_REQUEST)
            entity = Entity.objects.get(pk=data['entity_id'])
            db_property = Property.objects.get(pk=data['property_id'])
            update_column_type(schema, entity.entity_name, db_property.property_name, data['new_property_type'], data['required'], data['default_value'])
            db_property.property_type = data['new_property_type']
            db_property.save()
            return Response(None, status=status.HTTP_200_OK)
        return Response(update_property_type_model.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=DeletePropertySerializer)
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        renameEntityModel = DeletePropertySerializer(data=request.data)
        schema = get_tenant_schema(request)
        if(renameEntityModel.is_valid()):
            data = renameEntityModel.validated_data
            entity = Entity.objects.get(pk=data['entity_id'])
            db_property = Property.objects.get(pk=data['property_id'])
            remove_column(schema, entity.entity_name, db_property.property_name)
            db_property.delete()
            return Response(None, status=status.HTTP_200_OK)
        return Response(renameEntityModel.errors, status=status.HTTP_400_BAD_REQUEST)
