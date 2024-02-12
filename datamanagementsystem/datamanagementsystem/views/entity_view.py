from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..serializers.entity_serializer import EntitySerializer, RenameEntitySerializer, DeleteEntitySerializer, GetEntitySerializer
from ..helpers.schema_helper import get_tenant_schema, get_organization_id
from drf_yasg import openapi
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..services.entity_service import EntityService

search_text = openapi.Parameter('search_text', openapi.IN_QUERY,
                             description="search by entity or property name",
                             type=openapi.TYPE_STRING)

entity_service = EntityService()

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_entity(request, pk, format=None):
    entity_object = entity_service.get(pk)
    entity = GetEntitySerializer(entity_object)
    return Response(entity.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_entity(request, entity_id):
    schema = get_tenant_schema(request)
    entity_service.delete(schema, entity_id)
    return Response(None, status=status.HTTP_200_OK)

class EntityAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[search_text])
    def get(self, request):
        organization_id = get_organization_id(request)
        entity_objects = entity_service.get_all(organization_id, request.query_params.get('search_text'))
        entities = GetEntitySerializer(entity_objects, many=True)
        return Response(entities.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EntitySerializer)
    def post(self, request):
        entity = EntitySerializer(data=request.data)
        if(entity.is_valid()):
            organization_id = get_organization_id(request)
            schema = get_tenant_schema(request)
            entity_service.add(organization_id, schema, entity.validated_data)
            return Response(entity.data, status=status.HTTP_201_CREATED)
        return Response(entity.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(request_body=RenameEntitySerializer)
    def put(self, request):
        renameEntityModel = RenameEntitySerializer(data=request.data)
        schema = get_tenant_schema(request)
        if(renameEntityModel.is_valid()):
            validated_data = renameEntityModel.validated_data
            entity_service.rename(schema, validated_data)
            return Response(None, status=status.HTTP_200_OK)
        return Response(renameEntityModel.errors, status=status.HTTP_400_BAD_REQUEST)

            