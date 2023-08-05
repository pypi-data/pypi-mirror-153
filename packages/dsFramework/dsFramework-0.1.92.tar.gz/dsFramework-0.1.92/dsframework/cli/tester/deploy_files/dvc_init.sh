
# DONT RUN THIS if you checked out an exising project, dont run this.

# Initializes a DVC repository for this project.
# This is only run once, when a project is created.

# get repo name (see https://stackoverflow.com/questions/15715825/how-do-you-get-the-git-repositorys-name-in-some-git-repository)
#REPO_NAME=$(basename -s .git `git config --get remote.origin.url`)
DVC_BUCKET=gs://dozi-stg-ds-apps-1-ds-apps-ds-ml-artifacts
dvc init --no-scm
dvc config core.analytics false
dvc remote add --default ds-ml-artifacts ${DVC_BUCKET}/{name-your-service}
dvc remote modify ds-ml-artifacts projectname dozi-stg-ds-apps-1
