# serializers.py
from rest_framework import serializers
from .property_serializer import PropertySerializer

class SchemaSerializer(serializers.Serializer):
    schema_name = serializers.CharField(max_length=200)
    properties = PropertySerializer(many=True)
    class Meta:
        fields = '__all__'
