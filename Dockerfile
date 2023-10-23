FROM python:3.12-alpine as builder
ARG POETRY_VERSION="1.6.1"

WORKDIR /app
RUN apk add --no-cache gcc libffi-dev musl-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -q poetry=="${POETRY_VERSION}"
COPY . .
RUN poetry config virtualenvs.create false && poetry build -f wheel

FROM python:3.12-alpine

LABEL org.opencontainers.image.source="https://github.com/elisiariocouto/jsonschema-markdown"
LABEL org.opencontainers.image.authors="Elisiário Couto <elisiario@couto.io>"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="jsonschema-markdown"
LABEL org.opencontainers.image.description="Generate Markdown documentation from JSON Schema files"
LABEL org.opencontainers.image.url="https://github.com/elisiariocouto/jsonschema-markdown"

WORKDIR /app
COPY --from=builder /app/dist/ /app/
RUN pip --no-cache-dir install jsonschema*.whl && \
    rm jsonschema*.whl
ENTRYPOINT ["/usr/local/bin/jsonschema-markdown"]
