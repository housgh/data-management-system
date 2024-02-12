from ..helpers.sql_helper import update_column_name, add_column, update_column_type, remove_column
from ..models.entity import Entity
from ..exceptions.missing_default_value_exception import MissingDefaultValueException
from ..models.property import Property

class PropertyService:

    def add(self, organization_id, schema, validated_data):
        if(validated_data['required'] and validated_data.get('default_value') is None):
            raise MissingDefaultValueException()
        entity = Entity.objects.get(pk=validated_data['entity_id'], organization_id=organization_id)
        add_column(schema, entity.entity_name, validated_data)

    def rename(self, organization_id, schema, validated_data):
        entity = Entity.objects.get(pk=validated_data['entity_id'], organization_id=organization_id)
        db_property = Property.objects.get(pk=validated_data['property_id'], entity_id=entity.id)
        update_column_name(schema, entity.entity_name, db_property.property_name, validated_data['new_property_name'])
        db_property.property_name = validated_data['new_property_name']
        db_property.save()

    def change_type(self, organization_id, schema, validated_data):
        if(validated_data['required'] and validated_data.get('default_value') is None):
            raise MissingDefaultValueException()
        entity = Entity.objects.get(pk=validated_data['entity_id'], organization_id=organization_id)
        db_property = Property.objects.get(pk=validated_data['property_id'], entity_id=entity.id)
        update_column_type(
            schema, 
            entity.entity_name, 
            db_property.property_name, 
            validated_data['new_property_type_id'], 
            validated_data['required'], 
            validated_data.get('default_value'))
        
        db_property.property_type_id = validated_data['new_property_type_id']
        db_property.save()

    def delete(self, organization_id, schema, entity_id, id):
        entity = Entity.objects.get(pk=entity_id, organization_id=organization_id)
        db_property = Property.objects.get(pk=id, entity_id=entity.id)
        remove_column(schema, entity.entity_name, db_property.property_name)
        db_property.delete()