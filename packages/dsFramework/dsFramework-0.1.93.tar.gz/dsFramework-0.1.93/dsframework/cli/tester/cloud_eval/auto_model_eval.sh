#!/bin/sh
set -e

# This is the dataset name that will be used by CI/CD to evaluate your model. Please copy the name as it appears in DSP.
# example REFERENCE_DATASET="1600_sig_valid.csv"
export REFERENCE_DATASET="your_reference_dataset"

if [ REFERENCE_DATASET == "your_reference_dataset" ]; then
  echo "Find out and fill in your model reference dataset in file [cloud_eval/auto_model_eval.sh]. (You can ask the DSP Team for assistance)"
  exit 9
fi

# Load env params
source ./cloud_eval/.cloud_eval_env

./cloud_eval/eval_on_cloud_proc.sh $1 ${REFERENCE_DATASET}