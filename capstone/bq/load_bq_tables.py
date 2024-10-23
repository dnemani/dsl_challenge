from google.cloud import bigquery
from google.oauth2 import service_account
import google.auth
import os
import argparse

def load_table_from_csv(client, table_id, csv_path, write_disposition):
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip the header row
        write_disposition=write_disposition,
        autodetect=True  # Automatically detect the schema
    )
    job = client.load_table_from_uri(csv_path, table_id, job_config=job_config)
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
        project_id = credentials.project_id 

    client = bigquery.Client(credentials=credentials, project=project_id)
 
    dataset_id = 'default'  # Replace with your dataset ID
    tables = ['banks', 'fraud_transactions', 'merchants', 'transactions', 'users', 'sample_preproc_data']
    for table in tables:
        table_id = f'{project_id}.{dataset_id}.{table}'  # Replace with your table name
        # Load CSV file into BigQuery
        csv_path = f'gs://{project_id}/{table}/*'
        load_table_from_csv(client, table_id, csv_path, bigquery.WriteDisposition.WRITE_TRUNCATE)

if __name__ == "__main__":
    main()