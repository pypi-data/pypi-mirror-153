#--------- BEGIN DEVELOPER MODIFY FOR YOUR BUILD PROCESS ---------#
#Do not change the "AS build_image" part on the FROM
FROM python:3.8-slim AS build_image
#FROM docker.io/library/model_artifcats AS build_image
#Do not remove the BUILD_ACTION ARG, you can change its default value. You must use it in your build command in the RUN section for Jenkins to deploy your artifact.

# Define build arguments
ARG PIP_ACTION=install
ARG ARTIFACTORY_USERNAME
ARG ARTIFACTORY_PASSWORD
ARG GOOGLE_APPLICATION_CREDENTIALS

# Define environment variables
ENV GIT_PYTHON_REFRESH=quiet
ENV ARTIFACTORY_USR=$ARTIFACTORY_USERNAME
ENV ARTIFACTORY_PSW=$ARTIFACTORY_PASSWORD

#ENV TRANSFORMERS_CACHE='/app/.transformers_cache'

WORKDIR /app

# adding GOOGLE_APPLICATION_CREDENTIALS if passed using docker build --build-arg GOOGLE_APPLICATION_CREDENTIALS=
ADD $GOOGLE_APPLICATION_CREDENTIALS $GOOGLE_APPLICATION_CREDENTIALS

# Install basic packages and define virtual environment
RUN apt-get -o Acquire::Max-FutureTime=86400 update
RUN apt-get install -y --no-install-recommends build-essential gcc
RUN pip install --upgrade pip
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Install required packages for the image
ADD requirements_docker.txt /app/requirements_docker.txt
RUN pip ${PIP_ACTION} --no-cache-dir -r /app/requirements_docker.txt

# Add the application source code. Try to order them so that the folder which changes most would be last
ADD ./config /app/config
ADD ./pipeline_test.py /app
ADD ./dvc_download_artifacts.sh /app
ADD ./gunicorn.conf.py /app
ADD ./.dvcignore /app
ADD ./server /app/server
ADD ./tester /app/tester
ADD ./cloud_eval /app/cloud_eval
ADD ./pipeline /app/pipeline

# Define user and group
RUN groupadd -g 999 appuser && \
        useradd -r -d /app -u 999 -g appuser appuser
RUN chown -R appuser:appuser /app

# Switch to created user
USER appuser

# Download artifacts
RUN ["chmod", "+x", "/app/dvc_download_artifacts.sh"]
RUN ./dvc_download_artifacts.sh

# Perform basic end to end run of the pipeline in order to make sure that the build works well
RUN python /app/pipeline_test.py

#--------- END DEVELOPER MODIFY FOR YOUR BUILD PROCESS ---------#

#--------- BEGIN DEVELOPER MODIFY FOR YOUR DEPLOYMENT APP ---------#
#Do not change the "AS deploy_image" part of the FROM
FROM python:3.8-slim AS evaluation_image

MAINTAINER ZOOMINFO

WORKDIR /app

EXPOSE 8080/tcp
#Do not change "--from=build_image" it applies logic we us for our builds. sonar_scan will always have the same files as build_image
ENV PATH="/opt/venv/bin:$PATH"
ENV OMP_NUM_THREADS=2
ENV MKL_NUM_THREADS=2
ENV PYTORCH_INTEROP_THREADS=8
ENV ATEN_THREADING=TBB
RUN groupadd -g 999 appuser && \
        useradd -r -d /app -u 999 -g appuser appuser

COPY --from=build_image --chown=appuser:appuser /opt/venv /opt/venv
COPY --from=build_image --chown=appuser:appuser /app /app

USER appuser

FROM evaluation_image AS deploy_image
ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py", "server.main:app"]
#CMD ["gunicorn", "-k uvicorn.workers.UvicornWorker", "--log-file=-", "--graceful-timeout", "240", "--timeout", "120", "--bind=0.0.0.0:8080", "--workers=3", "server.main:app"]
#--------- END DEVELOPER MODIFY FOR YOUR DEPLOYMENT APP ---------#
