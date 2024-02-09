from django.db import connection

def create_db_schema(schema_name):
    execute_sql(f'CREATE SCHEMA {schema_name}')

def create_table(schema_name, table):
    table_name = table['schema_name']
    query = f'CREATE TABLE {schema_name}.{table_name} ('
    for index, db_property in enumerate(table['properties']):
        property_name = db_property['property_name']
        property_type = db_property['property_type']
        query = query + f'\n{property_name} {property_type}'
        if not db_property['nullable'] or db_property['primary_key']:
            query = query + ' not null'
        if index != len(table['properties']) - 1:
            query = query + ','
    query = query + '\n)'
    print(query)
    execute_sql(query) 

def add_column(schema_name, table_name, column_name, column_type):
    execute_sql(f'ALTER TABLE {schema_name}.{table_name} ADD {column_name} {column_type}')

def execute_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)