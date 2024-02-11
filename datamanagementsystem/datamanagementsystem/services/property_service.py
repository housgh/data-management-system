from ..helpers.sql_helper import update_column_name, add_column, update_column_type, remove_column
from ..models.entity import Entity
from ..exceptions.missing_default_value_exception import MissingDefaultValueException
from ..models.property import Property

class PropertyService:

    def add(self, schema, validated_data):
        if(validated_data['required'] and validated_data.get('default_value') is None):
            raise MissingDefaultValueException()
        entity = Entity.objects.get(pk=validated_data['entity_id'])
        add_column(schema, entity.entity_name, validated_data)

    def rename(self, schema, validated_data):
        entity = Entity.objects.get(pk=validated_data['entity_id'])
        db_property = Property.objects.get(pk=validated_data['property_id'])
        update_column_name(schema, entity.entity_name, db_property.property_name, data['new_property_name'])
        db_property.property_name = validated_data['new_property_name']
        db_property.save()

    def change_type(self, schema, validated_data):
        if(validated_data['required'] and validated_data.get('default_value') is None):
            raise MissingDefaultValueException()
        entity = Entity.objects.get(pk=validated_data['entity_id'])
        db_property = Property.objects.get(pk=validated_data['property_id'])
        update_column_type(
            schema, 
            entity.entity_name, 
            db_property.property_name, 
            validated_data['new_property_type'], 
            validated_data['required'], 
            validated_data['default_value'])
        
        db_property.property_type = validated_data['new_property_type']
        db_property.save()

    def delete(self, schema, validated_data):
        entity = Entity.objects.get(pk=validated_data['entity_id'])
        db_property = Property.objects.get(pk=validated_data['property_id'])
        remove_column(schema, entity.entity_name, db_property.property_name)
        db_property.delete()