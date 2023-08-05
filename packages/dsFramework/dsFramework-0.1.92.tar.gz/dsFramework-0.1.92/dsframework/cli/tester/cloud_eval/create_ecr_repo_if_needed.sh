## @file
## This script is part of the cloud evaluation scripts, its main purpose is to check if a repository exists in ECR,
## if not then create it.
##
## Uses the following command:
## @code
## aws ecr create-repository --repository-name "<ecr repo name>"
## @endcode
ECR_REPO_NAME={name-your-artifacts}

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${ECR_REPO_NAME}" > /dev/null 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${ECR_REPO_NAME}" > /dev/null
fi