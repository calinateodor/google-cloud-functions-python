from google.cloud import bigquery

def GCS_to_BQ(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    # Creating the file URI
    file_name = data['name']
    bucket_name = data['bucket']
    file_uri = 'gs://{}/{}'.format(bucket_name, file_name)

    # Configuring Load Job
    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig()
    dataset_name = 'YOUR_TARGET_DATASET_NAME'
    table_name = 'YOUR_TARGET_TABLE_NAME'
    table_ref = client.dataset(dataset_name).table(table_name)
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.skip_leading_rows = 1
    job_config.source_format = bigquery.SourceFormat.CSV
    table_schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('value', 'STRING')
    ]
    job_config.schema = table_schema

    # Checking if the table exists otherwise creates it
    try:
        client.get_table(table_ref)
    except:
        table = bigquery.Table(table_ref, schema=table_schema)
        table = client.create_table(table)  # API request

    # Creating Load Job
    load_job = client.load_table_from_uri(
        file_uri,
        table_ref,
        job_config=job_config)  # API request
    load_job.result()
    print('Load job finished')
