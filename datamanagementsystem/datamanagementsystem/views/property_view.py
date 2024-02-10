from rest_framework import status, viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..helpers.sql_helper import update_column_name, add_column, update_column_type, remove_column
from rest_framework_simplejwt.tokens import AccessToken
from ..serializers.property_serializer import PropertySerializer, UpdatePropertyNameSerializer, DeletePropertySerializer, UpdatePropertyTypeSerializer
from ..helpers.schema_helper import get_tenant_schema
from rest_framework.decorators import action


class PropertyAPIView(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=PropertySerializer)
    @action(detail=False, methods=['post'])
    def post(self, request):
        try:
            entity_property = PropertySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(entity_property.is_valid()):
                add_column(schema, entity_property.data)
                return Response(entity_property.data, status=status.HTTP_201_CREATED)
            return Response(entity_property.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(request_body=UpdatePropertyNameSerializer)
    @action(detail=False, methods=['put'])
    def update_name(self, request):
        try:
            update_property_name_model = UpdatePropertyNameSerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(update_property_name_model.is_valid()):
                data = update_property_name_model.data
                update_column_name(schema, data['entity_name'], data['old_property_name'], data['new_property_name'])
                return Response(None, status=status.HTTP_200_OK)
            return Response(update_property_name_model.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=UpdatePropertyTypeSerializer)
    @action(detail=False, methods=['put'])
    def update_type(self, request):
        try:
            update_property_type_model = UpdatePropertyTypeSerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(update_property_type_model.is_valid()):
                data = update_property_type_model.data
                update_column_type(schema, data['entity_name'], data['property_name'], data['new_property_type'])
                return Response(None, status=status.HTTP_200_OK)
            return Response(update_property_type_model.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(request_body=DeletePropertySerializer)
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        try:
            renameEntityModel = DeletePropertySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(renameEntityModel.is_valid()):
                data = renameEntityModel.data
                remove_column(schema, data['entity_name'], data['property_name'])
                return Response(None, status=status.HTTP_200_OK)
            return Response(renameEntityModel.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)