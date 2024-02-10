from django.db import connection

def create_db_schema(schema_name):
    execute_sql(f'CREATE SCHEMA {schema_name}')

def create_table(schema_name, table):
    table_name = table['entity_name']
    query = f'CREATE TABLE {schema_name}.{table_name} ('
    query = query + '\nid int primary key'
    if(len(table['properties']) != 0):
        query = query + ','
    for index, db_property in enumerate(table['properties']):
        property_name = db_property['property_name']
        property_type = db_property['property_type']
        query = query + f'\n{property_name} {property_type}'
        if db_property['required']:
            query = query + ' not null'
        if index != len(table['properties']) - 1:
            query = query + ','
    query = query + '\n)'
    print(query)
    execute_sql(query)

def rename_table(schema_name, old_table_name, new_table_name):
    execute_sql(f'ALTER TABLE {schema_name}.{old_table_name} RENAME TO {new_table_name}')

def delete_table(schema_name, table_name):
    execute_sql(f'DROP TABLE {schema_name}.{table_name}') 

def add_column(schema_name, table_name, column):
    column_name = column['column_name']
    column_type = column['column_type']
    query = f'ALTER TABLE {schema_name}.{table_name} ADD {column_name} {column_type}'
    if(column['required']):
        query = query + ' not null'
    execute_sql(query)

def remove_column(schema_name, table_name, column_name):
    execute_sql(f'ALTER TABLE {schema_name}.{table_name} DROP COLUMN {column_name}')

def update_column_name(schema_name, table_name, old_column_name, new_column_name):
    execute_sql(f'ALTER TABLE {schema_name}.{table_name} RENAME COLUMN {old_column_name} TO {new_column_name}')

def update_column_type(schema_name, table_name, column_name, new_column_type):
    execute_sql(f'ALTER TABLE {schema_name}.{table_name} ALTER COLUMN {column_name} TYPE {new_column_type}')



def execute_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)