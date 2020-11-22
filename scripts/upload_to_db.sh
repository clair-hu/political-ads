#!/usr/bin/env bash

export GOOGLE_APPLICATION_CREDENTIALS="cs348-group-project-2ddcf4e20dfb.json";
gcloud auth activate-service-account --key-file cs348-group-project-2ddcf4e20dfb.json
TOKEN="$(gcloud auth print-access-token)"

python3 scripts/upload_to_gcloud.py $1 $2 $TOKEN
