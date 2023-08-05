#export GOOGLE_APPLICATION_CREDENTIALS=/app/gcloud_credentials.json
export GIT_PYTHON_REFRESH=quiet
export GOOGLE_CLOUD_PROJECT='dozi-stg-ds-apps-1'
dvc init --no-scm
dvc remote add --default ds-ml-artifacts gs://dozi-stg-ds-apps-1-ds-apps-ds-ml-artifacts/{name-your-artifacts}
dvc remote modify ds-ml-artifacts projectname dozi-stg-ds-apps-1
dvc config core.analytics false

dvc status
dvc fetch
dvc pull
#python script_load_model.py
