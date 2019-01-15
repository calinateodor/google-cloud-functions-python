###Google Cloud Function to Load Different Files from Google Cloud Storage to Google BigQuery in Python

####Introduction
This cloud function loads CSV or JSON files from a Google Cloud bucket to BigQuery. Using the object.finalize trigger on the source bucket the function will load the data to BQ every time a new CSV is added to the source bucket.  
The function can be configured to load different files to different BQ tables based on the CSV file name.  

When a file is uploaded to GCS that matches a `file_name` in the `config.json`, the function will load the file to the specified `dataset_name.tabe_name` in the `config.json`.  

####Instructions:
1. Enable Cloud Functions, Cloud Storage and BigQuery APIs in the GCP Console.
2. Download the files from [here](https://github.com/calinateodor/google-cloud-functions-python/tree/master/gcs_to_bq_multi) 
3. Update `gcs_to_bq_multifile/config`
4. Add table schemas to `gcs_to_bq_multifile/schema` folder
5. Update `main.py` 
6. Update install.sh `--trigger-resource` flag with your source Cloud Storage bucket 
7. Open Cloud Shell in the GCP console
8. Run `./install.sh` 
9. Verify that the function is running in [GCP Console](https://console.cloud.google.com/functions)

####Structure of `config.json`
* `file_name`:
    * GCS object name of the source CSV  
* `dataset_name`:
    * name of the target BQ dataset
* table_name:
    * name of the target BQ table
* `schema_path `
    * path to the table schema in the deployment bucket
* `write_dispostion`:  
    * WRITE_TRUNCATE
    * WRITE_APPEND 
* `skip_leading_rows`:  
    * rows to skip from CSV file
* `source_format`:  
    * CSV
    * JSON

####Structure of schema files:
* For each column following parameters must be given:
    * `name`:
        * BQ column name
    * `field_type`:
        * BQ column type 
    * `mode`:
        * NULLABLE - column can have NULL values
        * REQUIRED - column cannot have NULL values
    * `description`:
        * Optional, leave empty if not needed
        * Column description
    * `fields`:
        * Needed only for `field_type: REPEATED`  
        * Leave empty list `[]` if field_type is different than REPEATED
