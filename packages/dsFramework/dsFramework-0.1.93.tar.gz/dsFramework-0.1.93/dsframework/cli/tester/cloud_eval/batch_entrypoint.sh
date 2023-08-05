#!/bin/bash
## @file
## This script is part of the cloud evaluation scripts, it does two main things:
## 1. Runs the server.
## 2. Runs dsframework/base/cloud_eval/worker.py
## with two parameters:
## @param $1 - input_dataset_path
## @param $2 - predictions_output_path
##
## @code
## python -m dsframework.base.cloud_eval.worker $1 $2
## @endcode

gunicorn -c cloud_eval/gunicorn.conf.py server.main:app
sleep 10
python -m dsframework.base.cloud_eval.worker $1 $2
