import json
from google.cloud import bigquery

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

def create_genres_table():
    # Initialize a BigQuery client
    client = bigquery.Client()

    # Define the dataset and table name
    dataset_id = 'your_dataset_id'  # Replace with your dataset ID
    table_id = f'{dataset_id}.genres'

    # Load the schema from the JSON file
    schema_json = load_schema_from_file('schema/genres.json')  # Replace with the path to your genres.json file

    # Create the BigQuery schema
    schema = create_bigquery_schema(schema_json)

    # Create a Table object
    table = bigquery.Table(table_id, schema=schema)

    # Create the table in BigQuery
    table = client.create_table(table)  # API request

    print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

# Call the function to create the table
create_genres_table()