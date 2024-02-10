from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..helpers.sql_helper import create_table, rename_table, delete_table
from rest_framework_simplejwt.tokens import AccessToken
from ..serializers.entity_serializer import EntitySerializer, RenameEntitySerializer, DeleteEntitySerializer
from ..helpers.schema_helper import get_tenant_schema


class EntityAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=EntitySerializer)
    def post(self, request):
        try:
            entity = EntitySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(entity.is_valid()):
                create_table(schema, entity.data)
                return Response(entity.data, status=status.HTTP_201_CREATED)
            return Response(entity.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(request_body=RenameEntitySerializer)
    def put(self, request):
        try:
            renameEntityModel = RenameEntitySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(renameEntityModel.is_valid()):
                data = renameEntityModel.data
                rename_table(schema, data['old_entity_name'], data['new_entity_name'])
                return Response(None, status=status.HTTP_200_OK)
            return Response(renameEntityModel.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(request_body=DeleteEntitySerializer)
    def delete(self, request):
        try:
            renameEntityModel = DeleteEntitySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(renameEntityModel.is_valid()):
                data = renameEntityModel.data
                delete_table(schema, data['entity_name'])
                return Response(None, status=status.HTTP_200_OK)
            return Response(renameEntityModel.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            