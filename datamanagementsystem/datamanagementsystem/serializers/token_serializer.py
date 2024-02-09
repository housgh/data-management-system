from ..models.user_details import get_by_user_id
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class TokenSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        userDetails = get_by_user_id(refresh['user_id'])
        
        print(userDetails)
        if userDetails is not None:
            refresh["organization_id"] = userDetails.organization_id

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data