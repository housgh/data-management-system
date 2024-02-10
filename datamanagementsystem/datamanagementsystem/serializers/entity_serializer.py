# serializers.py
from rest_framework import serializers
from .property_serializer import PropertySerializer

class EntitySerializer(serializers.Serializer):
    entity_name = serializers.CharField(max_length=200)
    properties = PropertySerializer(many=True)
    class Meta:
        fields = '__all__'

class RenameEntitySerializer(serializers.Serializer):
    old_entity_name = serializers.CharField(max_length=200)
    new_entity_name = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'

class DeleteEntitySerializer(serializers.Serializer):
    entity_name = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'


