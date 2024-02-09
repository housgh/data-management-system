from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..helpers.sql_helper import create_table
from rest_framework_simplejwt.tokens import AccessToken
from ..serializers.schema_serializer import SchemaSerializer
from ..helpers.schema_helper import get_tenant_schema


class SchemaAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=SchemaSerializer)
    def post(self, request):
        try:
            schema = SchemaSerializer(data=request.data)
            db_schema = get_tenant_schema(request)
            if(schema.is_valid()):
                create_table(db_schema, schema.data)
                return Response(schema.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            raise e