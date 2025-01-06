FROM --platform=linux/amd64 python:3.13-slim

# set environment
ENV PYTHONPATH="${PYTHONPATH}:/code/app"
ENV WORKPATH /code/app
ARG BUILD_ENV="prod"
ENV BUILD_ENV=$BUILD_ENV

# install requirements
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# install toolkits
RUN apt-get update && apt-get install -y curl vim build-essential

# copy codes to container
WORKDIR /code/app
COPY ./app /code/app

# copy wsgi/asgi config to container
ENV GUNICORN_CONF="/code/wsgi/gunicorn_config.py"
COPY wsgi/gunicorn_config.py /code/wsgi/gunicorn_config.py

# startup script
COPY ./startup/entrypoint.sh /entrypoint.sh
RUN chmod 777 /entrypoint.sh
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]