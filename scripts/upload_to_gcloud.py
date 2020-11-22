from google.cloud import storage

import argparse
import os
import requests


parser = argparse.ArgumentParser(description='Upload our csv files to gcloud')
parser.add_argument('tablename',help='name of sql table to insert data into')
parser.add_argument('filename',help='path to json file')
parser.add_argument('token', help='your authentication token')
args = parser.parse_args()

def upload_blob(source_file_name):
    """Uploads a file to the bucket."""
    bucket_name = "windy_marker_test_bucket"
    destination_blob_name = os.path.basename(source_file_name)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

upload_blob(args.filename)

upstream_url="https://www.googleapis.com/sql/v1beta4/projects/windy-marker-279018/instances/political-db/import"

json_object = {"importContext": {"fileType": "CSV","uri": "gs://windy_marker_test_bucket/" + os.path.basename(args.filename),"database": "us_political_ads","csvImportOptions":{"table": args.tablename}}}  

headers = {
    'Authorization' : 'Bearer ' +  args.token,
    'Content-Type': 'application/json; charset=utf-8'
}

response = requests.post(upstream_url, headers=headers, json=json_object)
print(response.text)

