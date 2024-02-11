from rest_framework import serializers
from ..models.property import Property

class PropertySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    entity_id = serializers.IntegerField()
    property_name = serializers.CharField(max_length=200)
    property_type = serializers.CharField(max_length=200)
    required = serializers.BooleanField()
    entity=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        fields = '__all__'
        model=Property

class CreatePropertySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    property_name = serializers.CharField(max_length=200)
    property_type = serializers.CharField(max_length=200)
    required = serializers.BooleanField()
    class Meta:
        fields = '__all__'

class UpdatePropertyNameSerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    property_id = serializers.IntegerField()
    new_property_name = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'

class UpdatePropertyTypeSerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    property_id = serializers.IntegerField()
    new_property_type = serializers.CharField(max_length=200)
    class Meta:
        fields = '__all__'

class DeletePropertySerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    property_id = serializers.IntegerField()
    class Meta:
        fields = '__all__'