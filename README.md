### Google Cloud Functions in Python  
This repository contains various Google Cloud Functions I wrote as proof of concept for different tasks.  
They can be adapted for specific needs  

* `gcs_to_bq`
    * loads a file from Cloud Storage to BigQuery in a predetermined table
    * function triggered by file upload to GCS
* `gcs_to_bq_multi`
    * loads files from GCS to BQ
    * based on a `config.json` GCS file names can be mapped to BQ tables such that a file with a specific name will be loaded to a specific table
    * Various other configuration options. For all the options check the README.md of the function. 
* `gcs_to_bq_pubsub`
    * same as `gcs_to_bq_multi`
    * additionally publishes on Google Pub/Sub 
        * if successful publishes on one topic
        * if error publishes on a different topic
    * publish message fully customizable
*  `web_crawler_to_bq` 
    * crawls a website, stores the data in a pandas dataframe and then uploads the dataframe to BQ
    * Wikipedia Toronto postal codes used as an example
