import requests
from google.cloud import bigquery
from google.oauth2 import service_account

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
    key_path = 'path/to/your-service-account-key.json'  # Replace with the path to your service account key file
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    project = 'your_project_id'  # Replace with your project ID
    dataset_id = 'your_dataset_id'  # Replace with your dataset ID
    table_id = f'{project}.{dataset_id}.genres'  # Replace with your table name

    # Download CSV file from GitHub
    csv_url = 'https://github.com/GoogleCloudPlatform/specialized-training-content/blob/main/courses/DSL/chinook-db/chinook-tables-csv/genres.csv?raw=true'
    csv_path = 'genres.csv'
    download_file(csv_url, csv_path)

    # Load CSV file into BigQuery
    load_table_from_csv(client, table_id, csv_path, bigquery.WriteDisposition.WRITE_TRUNCATE)

if __name__ == "__main__":
    main()