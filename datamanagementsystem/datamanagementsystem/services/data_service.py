from ..models.entity import Entity
from ..helpers.sql_helper import get_records, get_record, insert_records, delete_record, delete_all_records, update_record
from ..models.property import Property

class DataService:
    def get_all(self, schema, entity_id, skip, take, search_text):
        entity = Entity.objects.get(pk=entity_id)
        data = get_records(schema, entity.entity_name, skip, take, search_text)
        return data
    
    def get(self, schema, entity_id, id):
        entity = Entity.objects.get(pk=entity_id)
        data = get_record(schema, entity.entity_name, id)
        return data
    
    def delete(self, schema, entity_id, id):
        entity = Entity.objects.get(pk=entity_id)
        delete_record(schema, entity.entity_name, id)

    def delete_all(self, schema, entity_id):
        entity = Entity.objects.get(pk=entity_id)
        delete_all_records(schema, entity.entity_name)

    def add(self, schema, entity_id, validated_data):
        entity = Entity.objects.get(pk=entity_id)
        records = validated_data['records']
        data = []
        for dictionary in records:
            properties = Property.objects.filter(id__in=dictionary.keys()).all()
            data.append(dict([(property.property_name, dictionary[str(property.pk)]) for property in properties]))
        insert_records(schema, entity.entity_name, data)

    def update(self, schema, entity_id, id, validated_data):
        entity = Entity.objects.get(pk=entity_id)
        record = validated_data['record']
        properties = Property.objects.filter(id__in=record.keys()).all()
        data = dict([(property.property_name, record[str(property.pk)]) for property in properties])
        update_record(schema, entity.entity_name, id, data)