FROM python:3.7.6-alpine3.9 as development_build

LABEL maintainer="rfedorov@linkentools.com"
LABEL vendor="linkentools"

# System deps:
RUN apk --no-cache add build-base gcc libffi-dev postgresql-dev \
  && pip install poetry

WORKDIR /code
COPY . /code/

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
