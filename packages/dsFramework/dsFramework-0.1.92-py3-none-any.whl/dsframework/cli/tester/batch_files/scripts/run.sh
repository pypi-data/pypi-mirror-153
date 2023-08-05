#!/bin/bash
# export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
gcloud config set project dozi-data-science-research-1
bash ./batch_files/scripts/build.sh
dsf-cli upload-batch-files all
# python ./batch_files/workflow/auto_scaling_policy.py
dsf-cli workflow-template create
dsf-cli dag create
# dsf-cli dag import
# dsf-cli workflow-template instantiate
gcloud config set project dozi-stg-ds-apps-1
