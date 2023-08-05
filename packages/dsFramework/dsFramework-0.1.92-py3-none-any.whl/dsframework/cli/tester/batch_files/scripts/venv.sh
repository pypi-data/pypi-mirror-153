virtualenv env_1 -p python
source env_1/bin/activate  # activate virtualenv
env_1/bin/pip3 install -r requirements_docker.txt
# venv-pack -p env_1 -o venv_pack.tar.gz
# zip -r dist/environment.zip env_1
venv-pack -p env_1 -o dist/pyspark_venv.tar.gz -f
# env_1/bin/deactivate
