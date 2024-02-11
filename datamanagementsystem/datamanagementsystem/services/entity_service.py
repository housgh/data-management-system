from ..models.entity import Entity
from django.contrib.postgres.search import SearchVector
from ..helpers.sql_helper import create_table, rename_table, delete_table
from ..models.property import Property
from ..exceptions.missing_default_value_exception import MissingDefaultValueException

class EntityService:
    def get(self, id):
        entity_object = Entity.objects.prefetch_related('properties').get(pk=id)
        return entity_object
    
    def get_all(self, organization_id, search_text):
        if(search_text is not None):
            return Entity.objects.prefetch_related('properties').annotate(
                search=SearchVector('entity_name', 'properties__property_name')
                ).filter(search=search_text, organization_id=organization_id).all()
        return Entity.objects.prefetch_related('properties').all()
    
    def add(self, organization_id, schema, validated_data):
        for new_property in validated_data['properties']:
            if(new_property["required"] and new_property.get('default_value') is None):
                raise MissingDefaultValueException()
        create_table(schema, validated_data)
        new_entity = Entity.objects.create(entity_name=validated_data['entity_name'], organization_id=organization_id)
        for new_property in validated_data['properties']:
            Property.objects.create(entity=new_entity, **new_property)

    def rename(self, schema, validated_data):
        entity = Entity.objects.get(pk=validated_data['entity_id'])
        rename_table(schema, entity.entity_name, validated_data['new_entity_name'])
        entity.entity_name = validated_data['new_entity_name']
        entity.save()

    def delete(self, schema, validated_data):
        entity = Entity.objects.get(pk=validated_data['entity_id'])
        delete_table(schema, entity.entity_name)
        entity.delete()