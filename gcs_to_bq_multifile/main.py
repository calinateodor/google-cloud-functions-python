from google.cloud import bigquery
from google.cloud import storage
import json

def GCS_to_BQ_multifile(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This function loads a CSV file imported to Cloud Storage to Google BigQuery.
       Load job can be configured to import different CSVs to different BQ tables.
       Parameters are taken from config.json file and schema directory

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    # Creating the file URI
    bq_client = bigquery.Client()
    storage_client = storage.Client()

    file_name = data['name']
    upload_bucket_name = data['bucket']
    file_uri = 'gs://{}/{}'.format(upload_bucket_name, file_name)

    #Replace with the bucket where the code is stored on GCS
    deployment_bucket_name = storage_client.get_bucket('BUCKET_STORING_DEPLOYMENT_FILES')

    #Loading config file
    config_file_path = 'gcs_to_bq_multifile/config.json' #Path to config.json
    config_file_blob = deployment_bucket_name.get_blob(config_file_path)
    config_data = json.loads(config_file_blob.download_as_string())
    for config in config_data:
        if (config['file_name'] == file_name):
            table_name = config['table_name']
            dataset_name = config['dataset_name']
            schema_path = config['schema_path']
            write_disposition = config['write_disposition']
            skip_leading_rows = int(config['skip_leading_rows'])
            source_format = config['source_format']

    #Load Schema file
    schema_file_blob = deployment_bucket_name.get_blob(schema_path) #Load schema based on path in config.json
    table_schema = []
    schema_data = json.loads(schema_file_blob.download_as_string())
    for column in schema_data:
        column_schema = bigquery.SchemaField(name=column['name'], field_type=column['field_type'], mode=column['mode'], description=column['description'], fields=tuple(column['fields']))
        table_schema.append(column_schema)

    # Configuring Load Job
    job_config = bigquery.LoadJobConfig()
    table_ref = bq_client.dataset(dataset_name).table(table_name)
    if write_disposition == 'WRITE_TRUNCATE':
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    else:
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    if source_format == 'CSV':
        job_config.skip_leading_rows = skip_leading_rows
    if source_format == 'CSV':
        job_config.source_format = bigquery.SourceFormat.CSV
    elif source_format == 'JSON':
        job_config.source_format = bigquery.SourceFormat.JSON
    job_config.schema = table_schema

    # Checking if the table exists otherwise creates it
    try:
        bq_client.get_table(table_ref)
    except:
        table = bigquery.Table(table_ref, schema=table_schema)
        bq_client.create_table(table)  # API request

    # Creating Load Job
    load_job = bq_client.load_table_from_uri(
        file_uri,
        table_ref,
        job_config=job_config)  # API request
    load_job.result()
    print('Load job finished')
