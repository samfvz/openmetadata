from pprint import pp
import json
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest
from metadata.generated.schema.api.data.createDatabaseSchema import CreateDatabaseSchemaRequest
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.entity.data.table import Column, DataType, Table
from metadata.generated.schema.entity.services.databaseService import DatabaseService
from metadata.generated.schema.entity.data.database import Database
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema

server_config = OpenMetadataConnection(
    hostPort="http://localhost:8585/api",
    authProvider="openmetadata",
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken="ADD_YOUR_TOKEN"
    ),
)
metadata = OpenMetadata(server_config)
# Make sure we're connected to OM
assert metadata.health_check()

# Create or update new database
dbServiceFQDN = "local_postgres"
create_db = CreateDatabaseRequest(
    name="newDBSDK",
    service=dbServiceFQDN
)
create_db_entity = metadata.create_or_update(create_db)

# Create or update new schema
newSchemaName = "SDKSchema"
create_schema = CreateDatabaseSchemaRequest(
    name=newSchemaName,
    database=create_db_entity.fullyQualifiedName
)
create_schema_entity = metadata.create_or_update(data=create_schema)

# Create or update new table
newTableName = "SDKTable"
column1Name = "column1"
column1 = Column(name=column1Name, dataType=DataType.INT)
create_table = CreateTableRequest(
    name=newTableName,
    databaseSchema=create_schema_entity.fullyQualifiedName,
    columns=[column1]
)
create_table_entity = metadata.create_or_update(data=create_table)

# Print created objects
print("=============== DATABASE SERVICES: ===================")
listDatabaseServices = metadata.list_services(
    entity=DatabaseService
)
databaseService = listDatabaseServices[0]
pp(json.loads(databaseService.json()))

print("=============== DATABASES: ===================")
listDatabases = metadata.list_entities(
    entity=Database
)
pp(json.loads(listDatabases.json()))

print("=============== SCHEMAS: ===================")
listSchemas = metadata.list_entities(
    entity=DatabaseSchema
)
pp(json.loads(listSchemas.json()))

print("=============== TABLES: ===================")
listTables = metadata.list_entities(
    entity=Table
)
pp(json.loads(listTables.json()))
