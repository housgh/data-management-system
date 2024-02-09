from rest_framework_simplejwt.views import TokenViewBase
from ..serializers.token_serializer import TokenSerializer

class TokenView(TokenViewBase):
    serializer_class = TokenSerializer