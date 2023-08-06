ARG BASE_IMAGE=python:3.6-buster
FROM $BASE_IMAGE

# install project requirements
COPY src/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm -f /tmp/requirements.txt
RUN pip install git+https://bitbucket.org/indiciumtech/kedro_fast_api.git

# add kedro user
ARG KEDRO_UID=999
ARG KEDRO_GID=0
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
RUN groupadd -f -g ${KEDRO_GID} kedro_group && \
useradd -d /home/kedro -s /bin/bash -g ${KEDRO_GID} -u ${KEDRO_UID} kedro

# copy the whole project except what is in .dockerignore
WORKDIR /home/kedro
COPY . .
RUN chown -R kedro:${KEDRO_GID} /home/kedro
USER kedro
RUN chmod -R a+w /home/kedro
RUN python create_credentials_in_kedro.py
EXPOSE 8888
EXPOSE 8000

CMD ["kedro", "fast-api", "run"]
