import requests, json
from pprint import pp

header_auth = "Bearer ADD_YOUR_TOKEN"
base_url = "http://localhost:8585/api/v1"
json_content_type = "application/json"

api_request_headers = {
    "Authorization": header_auth
}


def send_get_request(api_url):
    request_url = f"{base_url}{api_url}"
    request = requests.get(
        url=request_url,
        headers=api_request_headers
    )
    response = request.json()

    return response


def send_put_request(api_url, payload):
    request_url = f"{base_url}{api_url}"
    request_header = api_request_headers
    request_header['Content-Type'] = json_content_type
    request = requests.put(
        url=request_url,
        headers=request_header,
        data=json.dumps(payload)
    )
    response = request.json()

    return response


# List bots
pp(send_get_request("/bots"))

# List databases
list_databases = send_get_request("/databases")
pp(list_databases)

# Create or update new database for existing service from a database above
databaseServiceName = list_databases.get('data')[0].get('service').get('name')
pp(databaseServiceName)
newDatabaseName = 'newDBApi'
newDatabaseApiPayload = {
    'name': newDatabaseName,
    'service': databaseServiceName
}
newDatabaseResponse = send_put_request("/databases", payload=newDatabaseApiPayload)
pp(newDatabaseResponse)
# Create or update schema in API-created database
DatabaseNameFQDN = newDatabaseResponse.get('fullyQualifiedName')
newDatabaseSchemaName = "APISchema"
newDatabaseSchemaAPIPayload = {
    'name': newDatabaseSchemaName,
    'database': DatabaseNameFQDN
}
newDatabaseSchemaResponse = send_put_request("/databaseSchemas", payload=newDatabaseSchemaAPIPayload)
pp(newDatabaseSchemaResponse)

# # Create or update new table in API-created database and schema
schemaFQDN = newDatabaseSchemaResponse.get('fullyQualifiedName')
newTableName = "APITable"
column1 = {
    "name": "column1",
    "dataType": "INT"
}

newTableAPIPayload = {
    "columns": [column1],
    "databaseSchema": schemaFQDN,
    "name": newTableName,
}
newTableResponse = send_put_request("/tables", payload=newTableAPIPayload)
pp(newTableResponse)
