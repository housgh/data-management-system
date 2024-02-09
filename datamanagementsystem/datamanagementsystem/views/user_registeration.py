from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.user_serializer import UserSerializer
from drf_yasg.utils import swagger_auto_schema

class UserRegistrationAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
