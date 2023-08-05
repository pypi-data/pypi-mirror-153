# run gcloud auth login if needed to be able to push to gcloud bucket
# gcloud auth login
dvc add --recursive pipeline/artifacts/vocabs
dvc add --recursive pipeline/artifacts/models
git add pipeline/artifacts/vocabs
git add pipeline/artifacts/models
git commit -m "Add data and artifacts to DVC"
dvc push
