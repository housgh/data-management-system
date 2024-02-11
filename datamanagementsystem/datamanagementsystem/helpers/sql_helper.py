from django.db import connection

def create_db_schema(schema_name):
    execute_sql('CREATE SCHEMA %s', schema_name)

def create_table(schema_name, table):
    table_name = table['entity_name']
    params = []
    query = f'CREATE TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" ('
    query += '\nid int primary key'
    if(len(table['properties']) != 0):
        query = query + ','
    for index, db_property in enumerate(table['properties']):
        property_name = db_property['property_name']
        property_type = db_property['property_type']
        query += f'\n"{sanitize(property_name)}" {property_type}'
        if db_property['required']:
            query += ' not null'
        if index != len(table['properties']) - 1:
            query += ','
    query += '\n)'
    execute_sql(query, *params)

def rename_table(schema_name, old_table_name, new_table_name):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(old_table_name)}" RENAME TO "{sanitize(new_table_name)}"')

def delete_table(schema_name, table_name):
    execute_sql(f'DROP TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}"') 

def add_column(schema_name, table_name, column):
    column_name = column['column_name']
    column_type = column['column_type']
    query = f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" ADD "{sanitize(column_name)}" {column_type}'
    if(column['required']):
        query = query + ' not null'
    execute_sql(query)

def remove_column(schema_name, table_name, column_name):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" DROP COLUMN "{sanitize(column_name)}"')

def update_column_name(schema_name, table_name, old_column_name, new_column_name):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" RENAME COLUMN "{sanitize(old_column_name)}" TO "{sanitize(new_column_name)}"', old_column_name, new_column_name)

def update_column_type(schema_name, table_name, column_name, new_column_type):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" ALTER COLUMN "{sanitize(column_name)}" TYPE {new_column_type}', column_name, new_column_type)

def get_records(schema_name, table_name, skip=None, take=None, search_text=None):
    params = []
    query = f'SELECT * FROM "{sanitize(schema_name)}"."{sanitize(table_name)}" as entity'
    if search_text is not None: 
        query += " WHERE entity::text LIKE %s"
        params.append(f'%{search_text}%')
    if skip is not None: 
        query += f' OFFSET {skip}'
        params.append(skip)
    if take is not None: 
        query += f' LIMIT {take}'
        params.append(take)
    return execute_get_all(query, *params)

def get_record(schema_name, table_name, id):
    query = f'SELECT * FROM "{sanitize(schema_name)}"."{sanitize(table_name)}" WHERE id=%s'
    return execute_get_one(query, id)

def execute_sql(sql, *arguments):
    with connection.cursor() as cursor:
        cursor.execute(sql, arguments)

def execute_get_all(query, *arguments):
    with connection.cursor() as cursor:
        cursor.execute(query, arguments)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def execute_get_one(query, *arguments):
    with connection.cursor() as cursor:
        cursor.execute(query, arguments)
        columns = [col[0] for col in cursor.description]
        return dict(zip(columns, cursor.fetchone()))
    
def sanitize(identifier):
    # Only allow alphanumeric characters, underscores, and dots
    # You may adjust this regex pattern based on your specific requirements
    import re
    return re.sub(r'[^\w.]', '', identifier)