from django.db import connection


property_types = {
    '1': 'varchar',
    '2': 'int',
    '3': 'decimal',
    '4': 'boolean',
    '5': 'date'
}

def create_db_schema(schema_name):
    execute_sql(f'CREATE SCHEMA "{sanitize(schema_name)}"')

def create_table(schema_name, table):
    table_name = table['entity_name']
    params = []
    query = f'CREATE TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" ('
    query += '\nid SERIAL PRIMARY KEY'
    if(len(table['properties']) != 0):
        query = query + ','
    for index, db_property in enumerate(table['properties']):
        property_name = db_property['property_name']
        property_type = property_types[str(db_property['property_type_id'])]
        query += f'\n"{sanitize(property_name)}" {property_type}'
        if db_property['required']:
            query += ' not null default %s'
            params.append(db_property['default_value'])
        if index != len(table['properties']) - 1:
            query += ','
    query += '\n)'
    execute_sql(query, *params)

def rename_table(schema_name, old_table_name, new_table_name):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(old_table_name)}" RENAME TO "{sanitize(new_table_name)}"')

def delete_table(schema_name, table_name):
    execute_sql(f'DROP TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}"') 

def add_column(schema_name, table_name, column):
    params = []
    column_name = column['property_name']
    column_type = property_types[str(column['property_type_id'])]
    query = f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" ADD "{sanitize(column_name)}" {column_type}'
    if(column['required']):
        query = query + ' not null default %s'
        params.append(column['default_value'])
    execute_sql(query *params)

def remove_column(schema_name, table_name, column_name):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" DROP COLUMN "{sanitize(column_name)}"')

def update_column_name(schema_name, table_name, old_column_name, new_column_name):
    execute_sql(f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" RENAME COLUMN "{sanitize(old_column_name)}" TO "{sanitize(new_column_name)}"')

def update_column_type(schema_name, table_name, column_name, new_column_type_id, required, default_value):
    params = []
    query = f'ALTER TABLE "{sanitize(schema_name)}"."{sanitize(table_name)}" ALTER COLUMN "{sanitize(column_name)}" TYPE {property_types[str(new_column_type_id)]}'
    if required:
        query += ' not null default %s'
        params.append(default_value)
    else:
        query += ' null'
    execute_sql(query, *params)

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

def insert_records(schema_name, table_name, data):
    query = f'INSERT INTO "{sanitize(schema_name)}"."{sanitize(table_name)}" ('
    properties = data[0].keys()
    query += ", ".join([f'"{sanitize(db_property)}"' for db_property in properties])
    query += ') VALUES '
    value_strings = []
    params = []
    for record in data:
        values = ["%s" for _ in range(0, len(properties))]
        params.extend([f"{record[prop]}" if isinstance(record[prop], str) else str(record[prop]) for prop in properties])
        value_strings.append("(" + ", ".join(values) + ")")
    query += ", ".join(value_strings)
    query += ";"
    print(query)
    execute_sql(query, *params)

def update_record(schema_name, table_name, id, data):
    params = []
    query = f'UPDATE "{sanitize(schema_name)}"."{sanitize(table_name)}" SET '
    for index, key in enumerate(data.keys()):
        query += f'{sanitize(key)} = %s '
        if(index != len(data.keys()) - 1):
            query += ','
        params.append(data[key])
    query += 'WHERE id = %s'
    params.append(id)
    execute_sql(query, *params)


def delete_record(schema_name, table_name, id):
    query = f'DELETE FROM "{sanitize(schema_name)}"."{sanitize(table_name)}" WHERE id=%s'
    execute_sql(query, id)

def delete_all_records(schema_name, table_name):
    query = f'DELETE FROM "{sanitize(schema_name)}"."{sanitize(table_name)}"'
    execute_sql(query)

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
    import re
    return re.sub(r'[^\w.]', '', identifier)