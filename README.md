### Google Cloud Functions in Python  
This repository contains various Google Cloud Functions I wrote.  

* gcs_to_bq
  * loads a file from Cloud Storage to BigQuery in a predetermined table
  * function triggered by file upload to GCS
* gcs_to_bq_multi
  * loads files from GCS to BQ
  * based on a `config.json` GCS file names can be mapped to BQ tables such that a file with a specific name will be loaded to a specific table
  * Various other configuration options. For all the options check the README.md of the function. 
