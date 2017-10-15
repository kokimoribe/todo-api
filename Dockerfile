# Reference documentation
# https://docs.docker.com/engine/reference/builder/

FROM python:3.6

RUN apt-get update && pip install --upgrade pip
WORKDIR /todo-api

COPY requirements.txt .
RUN pip install -r requirements.txt
