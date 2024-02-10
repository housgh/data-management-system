# serializers.py
from rest_framework import serializers

class PropertySerializer(serializers.Serializer):
    property_name = serializers.CharField(max_length=200)
    property_type = serializers.CharField(max_length=200)
    required = serializers.BooleanField()
    class Meta:
        fields = '__all__'

class UpdatePropertyNameSerializer(serializers.Serializer):
    entity_name = serializers.CharField(max_length=200)
    old_property_name = serializers.CharField(max_length=200)
    new_property_name = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'

class UpdatePropertyTypeSerializer(serializers.Serializer):
    entity_name = serializers.CharField(max_length=200)
    property_name = serializers.CharField(max_length=200)
    new_property_type = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'

class DeletePropertySerializer(serializers.Serializer):
    entity_name = serializers.CharField(max_length=200)
    property_name = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'