from ..models.organization import Organization
from ..serializers.organization_serializer import OrganizationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from ..helpers.sql_helper import create_db_schema
from rest_framework.permissions import AllowAny


class OrganizationAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=OrganizationSerializer)
    def post(self, request):
        organization = OrganizationSerializer(data=request.data)
        if organization.is_valid():
            create_db_schema(organization.validated_data['name'])
            organization.save()
            return Response(organization.data, status=status.HTTP_201_CREATED)
        return Response(organization.errors, status=status.HTTP_400_BAD_REQUEST)
        