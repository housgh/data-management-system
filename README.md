
# Data Management System

As part of the **ArabiaGIS K&A assessment**, We've created this project to **showcase my development & problem solving skills**. \
This project is written in *python* using the *Django framework* and runs a *Postgres* database for data persistence.

The objective of this project is to **create a multi-tenant data management system** where every tenant has a **secure, isolated environment to define, update, and
manage their data schemas dynamically**.
## Project Structure

The **project solution** has the following folder strucure:

```bash
datamanagementsystem
│   docker-compose.yml
│   dockerfile
│   manage.py
│   requirements.txt
│   
└───datamanagementsystem
    │   asgi.py
    │   settings.py
    │   urls.py
    │   wsgi.py
    │   __init__.py
    │
    ├───exceptions
    │       missing_default_value_exception.py
    │
    ├───helpers
    │   │   schema_helper.py
    │   │   sql_helper.py
    │   │   __init__.py
    │
    ├───middlewares
    │       exception_middleware.py
    │       __init__.py
    │
    ├───migrations
    │   │   __init__.py
    │
    ├───models
    │   │   entity.py
    │   │   organization.py
    │   │   property.py
    │   │   user_details.py
    │
    ├───serializers
    │   │   data_serializer.py
    │   │   entity_serializer.py
    │   │   organization_serializer.py
    │   │   property_serializer.py
    │   │   token_serializer.py
    │   │   user_serializer.py
    │   │   __init__.py
    │
    ├───services
    │   |   data_service.py
    │   |   entity_service.py
    │   |   property_service.py
    │   |   __init__.py
    │
    ├───views
    │   │   data_view.py
    │   │   entity_view.py
    │   │   organization_view.py
    │   │   property_view.py
    │   │   token_view.py
    │   │   user_registeration.py
    │   │   __init__.py
```
## Running the Project

To insure that the project **runs anywhere without worrying about the project dependencies**, a `Dockerfile` has been associated with the project which includes all the necessary dependencies.\
The project also contains a `docker-compose.yml` file that contains the following services:
- **datamanagementsystem** (runs on port 8000 - exposed)
- **postgres** (runs on port 5432 - not exposed)
- **pgadmin** (runs on port 5050 - exposed)
If any of these ports are not available on your device, we can always change the values in the `docker-compose.yml` under the `ports` section of each service.

To get started, we have to make sure that **`Docker` is installed on our device** by running the following command:
```bash
$ docker --version
```
If it is not installed, **you can download it from the following link**:\
https://docs.docker.com/get-docker/

Once installed, **navigate to the location of the `docker-compose.yml` file and run the following command**:
```bash
$ docker compose up -d --build
```
This will spin off the three services and will automatically migrate the changes into the database.

To **shut down the application**, in the `docker-compose.yml` directory run the following command:
```bash
$ docker compose down
```
## API Documentation

This application uses the **OpenAPI specifications**.

Once our `docker-compose.yml` is running, we will have two API Documentation pages:\
Head to *http://localhost:8000/redoc* for the **API documentation**.\
You can also head to *http://localhost:8000/swagger* to **interact with the application endpoints**.

## Data Management System Guide
### Creating an Organization

To start using the system, first we need to **create an organization** (Tenant). We can do that by executing the `/Organization` POST endpoint while specifying the `name` and `address` of our new organization.

### Registering a User

Next, we need to **create our user**. We can do that by executing the `/register` POST endpoint. Here is a sample request body:
```json
{
  "username": "user",
  "password": "P@ssw0rd",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "organization_id": 1
}
```
### Creating a Token

The data management system uses *JWT Authentication* to **insure that the data is secure and isolated between organizations**.

To **generate a token**, we can use the `/token` POST endpoint and specifying the `username` and `password` we used while registering. Once executed, we will recieve the following response:

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNzgyMDY5MiwiaWF0IjoxNzA3NzM0MjkyLCJqdGkiOiI0ZWJjYzVkMDlhMjA0ZmNjYmQ3ZjM0NTAxMjJmYjYwNyIsInVzZXJfaWQiOjEsIm9yZ2FuaXphdGlvbl9pZCI6MX0.n-xSNyR1blbSU_Q8BpQI6ORHTJPNMtyxoaPcZcsLkMw",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA3ODIwNjkyLCJpYXQiOjE3MDc3MzQyOTIsImp0aSI6IjAxMGVjMDViYjg1MDQ1MGFhNzAxOTU1NzdiOTA1NjJlIiwidXNlcl9pZCI6MSwib3JnYW5pemF0aW9uX2lkIjoxfQ.lKlTmSD6abZ9Y7Y7KAGLLlUVd6EA_CR51Vtd_8FcdO0"
}
```

We will use the **`access` property as our access token**. If you are using swagger, click on the *Authorize* button in the top right corner, and in the value field insert following:
```
Bearer {your-access-token}
```
Replacing `{your-access-token}` with the access token generated above. To **authenticate your requests outside swagger** we can specify the `Authorization` header with the same value.


The access **token lifetime** is 1 hour. However, **it should be shorter in production environments**. We can update the lifetime in the `settings.py` file by updating `ACCESS_TOKEN_LIFETIME` setting.

Once we have the token, we will have access to the `Entity` and `Data` endpoints.

### Data Management

In terms of a Postgres database, **each organization will have its own database schema**, insuring isolation between the organizations.

The public (default) schema will contain the common tables between the organizations such as the organizations, users, entity definitions, and property definitions.

Each schema will contain multiple tables (entities) specific to the organization, and each table will contain multiple column (property).

#### Entities

In the `Entity` endpoints, we have the ability to **create, rename, get**, and **delete** all entities. Below is a sample request body for creating an entity:
```json
{
  "entity_name": "my_entity",
  "properties": [
    {
      "property_name": "name",
      "property_type_id": 1,
      "required": true,
      "default_value": "default_value"
    },
    {
      "property_name": "amount",
      "property_type_id": 2,
      "required": true,
      "default_value": 0
    },
  ]
}
```

_An id property is not required and is automatically created and set as primary key when creating an entity_.

For security reasons, the **property types have been limited to the following dictionary**:

```python
property_types = {
    '1': 'varchar',
    '2': 'int',
    '3': 'decimal',
    '4': 'boolean',
    '5': 'date'
}
```
However, more types can be included in the dictionary if needed.

#### Properties

We can also **manage the `properties` under any entity** using the `/entity/property/` endpoints. We can **create, rename, change type**, and **delete** any property. Below is a sample request body for creating a property:

```json
{
  "entity_id": 0,
  "property_name": "string",
  "property_type_id": 1,
  "required": true,
  "default_value": "string"
}
```

_The system will adapt to these changes in realtime_.

#### Data

After creating our entities/properties, we need to **populate our entities with data**. We can achieve this by **using the `data` endpoints**, where we can **create, update, read**, and **delete** records from the table.

To **create a record** in the table, we can use the `/data/insert/{entity_id}` POST endpoint. Below is a sample request body:

```json
{
  "records": [
    {
      "1": "some_name",
      "2": 1,
    }
  ]
}
```

Where each member of the `records` array is a row in the table consisting of a dictionary where each key is a property_id and the value is the value we need to insert for this property.
## Security Measures

To insure that all the **data is perfectly secured**, multiple security measure have been taken, including **data isolation, JWT authentication, SQL query sanitization**, and **global exception handling**.

### Data Isolation

**Each organization has its own schema in the Postgres** wich insures that the data does not get mixed up or exposed between organizations.

### JWT Authentication

To prevent unauthorized access to another organization's data, a **JWT access token is required to access the desired organization entities and data**. The access token will help the system know who is the user accessing the data and to which organization this user belongs to.

### SQL Query Sanitization

Since we went with the Raw SQL approach for the schema manipulation, we face a risk of SQL **injection attacks**. To prevent this, **query parameters were used** where possible, and where not possible, **manual sanitization was applied** by removing all characters except alphanumeric values, underscores, and dots.

### Global Exception Handling

We also implemented a **global exception handling** middleware that insures than **any unhandled exception is not returned to the public** which might expose sensitive information about the application.
## PgAdmin

The `docker-compose.yml` includes a **pgAdmin service** so we can view the database in realtime.

To access the pgAdmin portal, we can go to *http://localhost:5050*, then we login with the following credentials:
 - **email:** admin@example.com
 - **password:** adminpassword

Next, we need to add our `Postgres` server to the avaialble servers. We can do that by right clicking on Servers then clicking `Register > Server...` .

In the General tab, set a name for your server (ex: datamanagementsystem), then navigate to the Connection tab and set the following:
- **Host:** postgres
- **Port:** 5432
- **Username:** admin
- **Password:** P@ssw0rd

Then click Save to add your server where you will be able to access all the schemas.



## Future Considerations

To better secure the application, We believe that Raw SQL should be replaced with a dynamic ORM. However this requires some research to check the possibility of this enhancement 