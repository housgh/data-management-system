# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.user_details import UserDetails
from ..models.organization import Organization

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    organization_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'organization_id')

    def create(self, validated_data):
        print(validated_data['organization_id'])
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        userDetails = UserDetails.objects.create(user=user, organization_id=validated_data['organization_id'])
        return user