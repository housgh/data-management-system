# serializers.py
from rest_framework import serializers

class PropertySerializer(serializers.Serializer):
    schema_name = serializers.CharField(max_length=200)
    property_name = serializers.CharField(max_length=200)
    property_type = serializers.CharField(max_length=200)
    primary_key = serializers.BooleanField()
    nullable = serializers.BooleanField()
    class Meta:
        fields = '__all__'
