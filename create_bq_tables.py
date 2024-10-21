import json
from google.cloud import bigquery
from google.oauth2 import service_account

def load_schema_from_file(file_path):
    with open(file_path, 'r') as file:
        schema_json = json.load(file)
    return schema_json

def create_bigquery_schema(schema_json):
    schema = []
    for field in schema_json:
        schema.append(bigquery.SchemaField(
            name=field['name'],
            field_type=field['type'],
            mode=field.get('mode', 'NULLABLE')
        ))
    return schema

def create_bigquery_dataset(client, dataset_id):

    dataset_id = f"{client.project}.{dataset_id}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset, exists_ok=True)  # API request
    print(f"Created dataset {client.project}.{dataset.dataset_id}")

def create_table(client,table_name, dataset_id):

    table_id = f'{client.project}.{dataset_id}.{table_name}'

    # Load the schema from the JSON file
    schema_json = load_schema_from_file(f'schema/{table_name}.json')  # Replace with the path to your genres.json file

    # Create the BigQuery schema
    schema = create_bigquery_schema(schema_json)

    # Create a Table object
    table = bigquery.Table(table_id, schema=schema)

    # Create the table in BigQuery
    table = client.create_table(table,exists_ok=True)  # API request

    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")


# Path to your service account key file
key_path = 'qwiklabs-gcp-00-cc9e35073c89-02d2bd1ed53b.json'  # Replace with the path to your service account key file

# Authenticate using the service account key file
credentials = service_account.Credentials.from_service_account_file(key_path)

print(f"Project Id {credentials.project_id}")

# Initialize a BigQuery client with the credentials
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# Define the dataset and table name
dataset_id = 'default'  # Replace with your dataset ID

# Create the dataset
create_bigquery_dataset(client, dataset_id)

# create a for loop to create tables in schema subfolder
tables = ['albums', 'artists', 'customers', 'employees', 'genres', 'invoice_items', 'invoices', 'media_types', 'playlists', 'playlist_track', 'tracks']

for table_name in tables:
    create_table(client, table_name, dataset_id)

