from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.property_serializer import (
    PropertySerializer, 
    UpdatePropertyNameSerializer, 
    DeletePropertySerializer, 
    UpdatePropertyTypeSerializer)
from ..helpers.schema_helper import get_tenant_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from ..services.property_service import PropertyService

property_service = PropertyService()

class PropertyAPIView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PropertySerializer)
    @action(detail=False, methods=['post'])
    def post(self, request):
        entity_property = PropertySerializer(data=request.data)
        if(entity_property.is_valid()):
            schema  = get_tenant_schema(request)
            validated_data = entity_property.validated_data
            property_service.add(schema, validated_data)
            entity_property.save()
            return Response(entity_property.validated_data, status=status.HTTP_201_CREATED)
        return Response(entity_property.validated_datas, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=UpdatePropertyNameSerializer)
    @action(detail=False, methods=['put'])
    def update_name(self, request):
        update_property_name_model = UpdatePropertyNameSerializer(data=request.data)
        if(update_property_name_model.is_valid()):
            schema = get_tenant_schema(request)
            validated_data = update_property_name_model.validated_data
            property_service.rename(schema, validated_data)
            return Response(None, status=status.HTTP_200_OK)
        return Response(update_property_name_model.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UpdatePropertyTypeSerializer)
    @action(detail=False, methods=['put'])
    def update_type(self, request):
        update_property_type_model = UpdatePropertyTypeSerializer(data=request.data)
        if(update_property_type_model.is_valid()):
            schema = get_tenant_schema(request)
            validated_data = update_property_type_model.validated_data
            property_service.change_type(schema, validated_data)
            return Response(None, status=status.HTTP_200_OK)
        return Response(update_property_type_model.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['delete'], url_path='<int:entity_id>/<int:id>')
    def delete(self, request, entity_id, id):
        schema = get_tenant_schema(request)
        property_service.delete(schema, entity_id, id)
        return Response(None, status=status.HTTP_200_OK)
