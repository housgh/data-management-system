from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..helpers.sql_helper import create_table, rename_table, delete_table
from ..serializers.entity_serializer import EntitySerializer, RenameEntitySerializer, DeleteEntitySerializer, GetEntitySerializer
from ..helpers.schema_helper import get_tenant_schema, get_organization_id
from ..models.entity import Entity
from ..models.property import Property
import traceback
from django.contrib.postgres.search import SearchVector
from drf_yasg import openapi
from rest_framework.decorators import api_view


search_text = openapi.Parameter('search_text', openapi.IN_QUERY,
                             description="search by entity or property name",
                             type=openapi.TYPE_STRING)

@api_view(['GET'])
def get_entity(request, pk, format=None):
    try:
        entityObject = Entity.objects.prefetch_related('properties').get(pk=pk)
        entity = GetEntitySerializer(entityObject)
        return Response(entity.validated_data, status=status.HTTP_200_OK)
    except Entity.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class EntityAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(manual_parameters=[search_text])
    def get(self, request):
        if('search_text' in request.query_params):
            search_text = request.query_params['search_text']
            print(search_text)
            entityObjects = Entity.objects.prefetch_related('properties').annotate(
            search=SearchVector('entity_name', 'properties__property_name')
            ).filter(search=search_text).all()
        else:
            entityObjects = Entity.objects.prefetch_related('properties').all()
        entities = GetEntitySerializer(entityObjects, many=True)
        return Response(entities.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EntitySerializer)
    def post(self, request):
        try:
            entity = EntitySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(entity.is_valid()):
                create_table(schema, entity.validated_data)
                organization_id = get_organization_id(request)
                new_entity = Entity.objects.create(entity_name=entity.validated_data['entity_name'], organization_id=organization_id)
                for new_property in entity.validated_data['properties']:
                    Property.objects.create(entity=new_entity, **new_property)
                return Response(entity.validated_data, status=status.HTTP_201_CREATED)
            return Response(entity.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            print(traceback.format_exc())
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(request_body=RenameEntitySerializer)
    def put(self, request):
        try:
            renameEntityModel = RenameEntitySerializer(data=request.data)
            schema = get_tenant_schema(request)
            if(renameEntityModel.is_valid()):
                data = renameEntityModel.validated_data
                entity = Entity.objects.get(pk=data['entity_id'])
                rename_table(schema, entity.entity_name, data['new_entity_name'])
                entity.entity_name = data['new_entity_name']
                entity.save()
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
                data = renameEntityModel.validated_data
                entity = Entity.objects.get(pk=data['entity_id'])
                delete_table(schema, entity.entity_name)
                entity.delete()
                return Response(None, status=status.HTTP_200_OK)
            return Response(renameEntityModel.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(repr(e))
            return Response('An Error Has Occured.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            