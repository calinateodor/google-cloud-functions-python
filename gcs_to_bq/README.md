### Google Cloud Function to Load Data from Google Cloud Storage to Google BigQuery in Python

#### Introduction
This cloud function loads CSV or JSON files from a Google Cloud bucket to BigQuery. Using the object.finalize trigger on the source bucket the function will load the data to BQ every time a new CSV is added to the source bucket.  

#### Instructions:
1. Enable Cloud Functions, Cloud Storage and BigQuery APIs in the GCP Console.
2. Download the files from [here](https://github.com/calinateodor/google-cloud-functions-python/tree/master/gcs_to_bq) 
3. Update `main.py` with BQ dataset name, BQ table name, and BQ table schema  
4. Update install.sh `--trigger-resource` flag with your source Cloud Storage bucket   
5. Open Cloud Shell in the GCP console
6. Run `./install.sh` 
7. Verify that the function is running in [GCP Console](https://console.cloud.google.com/functions)
