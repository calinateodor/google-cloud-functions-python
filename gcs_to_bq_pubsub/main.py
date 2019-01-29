from google.cloud import bigquery
from google.cloud import pubsub_v1
import json
from load_job import LoadtoBQ as ltbq
from publish import PublishTopic as publish


def gcs_to_bq(data, context):
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

    project_id = 'PROJECT_ID' # Add project ID
    success_topic_name = 'bq-upload-success' # Add pub sub topic name
    error_topic_name = 'bq-upload-error' # Add pub sub topic name

    # Success message variables
    file_name = data['name']
    upload_bucket_name = data['bucket']
    config_file_path = 'config.json'
    with open(config_file_path) as config_file:
        config_data = json.load(config_file)
    for config in config_data:
        if config['file_name'] == file_name:
            table_name = config['table_name']
            dataset_name = config['dataset_name']

    #Load and post result
    try:
        ltbq().load_to_bq(data, context)
        data_package = u'File gs://{}/{} successfully loaded to {}.{}'.format(upload_bucket_name, file_name, dataset_name, table_name)
        data_package.encode('utf-8')
        publish().publisher(project_id, success_topic_name, data_package)
    except Exception as err:
        error_package = str(err).encode('utf-8')
        publish().publisher(project_id, error_topic_name, error_package)
