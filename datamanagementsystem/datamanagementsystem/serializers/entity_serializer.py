# serializers.py
from rest_framework import serializers
from .property_serializer import CreatePropertySerializer, PropertySerializer
from ..models.entity import Entity

class EntitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    entity_name = serializers.CharField(max_length=200)
    properties = CreatePropertySerializer(many=True)
    organization=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        fields = '__all__'
        model = Entity

class GetEntitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    entity_name = serializers.CharField(max_length=200)
    properties = PropertySerializer(many=True)
    class Meta:
        fields = '__all__'
        model = Entity

        

class RenameEntitySerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    new_entity_name = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'

class DeleteEntitySerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    class Meta:
        fields = '__all__'


