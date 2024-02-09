# serializers.py
from rest_framework import serializers
from ..models.organization import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Organization
        fields = ('id', 'name', 'address')