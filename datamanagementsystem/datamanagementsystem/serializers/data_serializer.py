from rest_framework import serializers

class DataSerializer(serializers.Serializer):
    records = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))
    class Meta:
        fields = '__all__'

class UpdateDataSerializer(serializers.Serializer):
    record=serializers.DictField(child=serializers.CharField())
    class Meta:
        fields = '__all__'
