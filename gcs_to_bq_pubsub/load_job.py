from google.cloud import bigquery
import json


class LoadtoBQ(object):
    def load_to_bq(self, data, context):
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
        file_name = data['name']
        upload_bucket_name = data['bucket']
        file_uri = 'gs://{}/{}'.format(upload_bucket_name, file_name)

        #Loading config file
        config_file_path = 'config.json'
        with open(config_file_path) as config_file:
            config_data = json.load(config_file)
        for config in config_data:
            if config['file_name'] == file_name:
                table_name = config['table_name']
                dataset_name = config['dataset_name']
                schema_path = config['schema_path']
                write_disposition = config['write_disposition']
                skip_leading_rows = int(config['skip_leading_rows'])
                source_format = config['source_format']

        #Load Schema file
        with open(schema_path) as schema_file:
            schema_data = json.load(schema_file)
        table_schema = []
        for column in schema_data:
            column_schema = bigquery.SchemaField(name=column['name'], field_type=column['field_type'], mode=column['mode'], description=column['description'], fields=tuple(column['fields']))
            table_schema.append(column_schema)

        # Configuring Load Job
        client = bigquery.Client()
        job_config = bigquery.LoadJobConfig()
        table_ref = client.dataset(dataset_name).table(table_name)
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
            client.get_table(table_ref)
        except:
            table = bigquery.Table(table_ref, schema=table_schema)
            client.create_table(table)  # API request

        # Creating Load Job
        load_job = client.load_table_from_uri(
            file_uri,
            table_ref,
            job_config=job_config)  # API request
        load_job.result()
        print('Load job finished')
