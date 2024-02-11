from rest_framework import serializers

class DataSerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    records = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))
    class Meta:
        fields = '__all__'
