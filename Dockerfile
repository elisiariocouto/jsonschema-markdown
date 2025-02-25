FROM python:3.13-alpine AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --no-group dev

FROM python:3.13-alpine

LABEL org.opencontainers.image.source="https://github.com/elisiariocouto/jsonschema-markdown"
LABEL org.opencontainers.image.authors="Elisiário Couto <elisiario@couto.io>"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="jsonschema-markdown"
LABEL org.opencontainers.image.description="Generate Markdown documentation from JSON Schema files"
LABEL org.opencontainers.image.url="https://github.com/elisiariocouto/jsonschema-markdown"

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv

ENTRYPOINT ["/app/.venv/bin/jsonschema-markdown"]
