FROM python:3.11-alpine

LABEL maintainer="Elisiário Couto  <elisiario@couto.io>"
LABEL org.label-schema.vcs-url="https://github.com/elisiariocouto/jsonschema-markdown"

ARG POETRY_VERSION="1.5.1"

RUN /usr/local/bin/python -m pip install -q --upgrade pip && \
    pip install --no-cache-dir -q poetry=="${POETRY_VERSION}"

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --without=dev

ENTRYPOINT [ "jsonschema-markdown" ]
