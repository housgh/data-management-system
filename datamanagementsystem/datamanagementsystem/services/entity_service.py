from ..models.entity import Entity
from django.contrib.postgres.search import SearchVector
from ..helpers.sql_helper import create_table, rename_table, delete_table
from ..models.property import Property
from ..exceptions.missing_default_value_exception import MissingDefaultValueException

class EntityService:
    def get(self, organization_id, id):
        entity_object = Entity.objects.prefetch_related('properties').get(pk=id, organization_id=organization_id)
        return entity_object
    
    def get_all(self, organization_id, search_text):
        if(search_text is not None):
           entity_name_filter = Entity.objects.filter(entity_name__icontains=search_text)
           properties_name_filter = Entity.objects.prefetch_related('properties').filter(properties__property_name__icontains=search_text)
           filter = entity_name_filter | properties_name_filter
           return filter.filter(organization_id=organization_id).distinct().all()
        return Entity.objects.prefetch_related('properties').filter(organization_id=organization_id).all()
    
    def add(self, organization_id, schema, validated_data):
        for new_property in validated_data['properties']:
            if(new_property["required"] and new_property.get('default_value') is None):
                raise MissingDefaultValueException()
        create_table(schema, validated_data)
        new_entity = Entity.objects.create(entity_name=validated_data['entity_name'], organization_id=organization_id)
        for new_property in validated_data['properties']:
            Property.objects.create(entity=new_entity, **new_property)

    def rename(self, organization_id, schema, validated_data):
        entity = Entity.objects.get(pk=validated_data['entity_id'], organization_id=organization_id)
        rename_table(schema, entity.entity_name, validated_data['new_entity_name'])
        entity.entity_name = validated_data['new_entity_name']
        entity.save()

    def delete(self, organization_id, schema, entity_id):
        entity = Entity.objects.get(pk=entity_id, organization_id=organization_id)
        delete_table(schema, entity.entity_name)
        entity.delete()