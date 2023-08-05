#!/bin/sh

#cli_file_dest=[]

## @file
## Cloud evaluation entry point.
## It basically runs a dataset on a specific model version on an AWS cloud service and returns results.
## It executes eval_on_cloud_proc.sh script with the following parameters:
## @param $1 Tag to the required version
## @param $2 Dataset file path
## @param $3 State machine - prd, stg or dev
##
## @code
## ./cloud_eval/eval_on_cloud_proc.sh $1 $2 $3
## @endcode
##

set -e

./cloud_eval/eval_on_cloud_proc.sh $1 $2 $3