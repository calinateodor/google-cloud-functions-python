#!/bin/bash

#update TRIGGER_BUCKET_NAME with source bucket
gcloud functions deploy GCS_to_BQ --trigger-resource TRIGGER_BUCKET_NAME --trigger-event google.storage.object.finalize
