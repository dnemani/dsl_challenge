import requests
from google.cloud import bigquery
from google.oauth2 import service_account
import os
import argparse

def download_file(url, local_path):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    with open(local_path, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded file to {local_path}")

def load_table_from_csv(client, table_id, csv_path, write_disposition):
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip the header row
        write_disposition=write_disposition,
        autodetect=True  # Automatically detect the schema
    )
    with open(csv_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete
    print(f"Loaded {table_id} with {job.output_rows} rows")

def main():


    # Check if the code is running in Google Cloud Shell
    cloud_shell = os.getenv('GOOGLE_CLOUD_SHELL')
    if cloud_shell:
        credentials, project_id = google.auth.default()
        client = bigquery.Client(credentials=credentials, project=project_id)
    else:

        parser = argparse.ArgumentParser(description='Create BigQuery tables from schema files.')
        parser.add_argument('--key_path', required=True, help='Path to the service account key file')
        args = parser.parse_args()

        key_path = args.key_path

        # Authenticate using the service account key file   
        credentials = service_account.Credentials.from_service_account_file(key_path)
        client = bigquery.Client(credentials=credentials, project=project_id)
        project_id = credentials.project_id 
 
    dataset_id = 'default'  # Replace with your dataset ID
    tables = ['albums', 'artists', 'customers', 'employees', 'genres', 'invoice_items', 'invoices', 'media_types', 'playlists', 'playlist_track', 'tracks']
    for table in tables:
        table_id = f'{project_id}.{dataset_id}.{table}'  # Replace with your table name

    # Download CSV file from GitHub

        csv_url = f'https://github.com/GoogleCloudPlatform/specialized-training-content/blob/main/courses/DSL/chinook-db/chinook-tables-csv/{table}.csv?raw=true'
        print(csv_url)
        csv_path = f'{table}.csv'
        download_file(csv_url, csv_path)

    # Load CSV file into BigQuery
        load_table_from_csv(client, table_id, csv_path, bigquery.WriteDisposition.WRITE_TRUNCATE)

if __name__ == "__main__":
    main()