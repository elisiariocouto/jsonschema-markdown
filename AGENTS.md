# AGENTS.md

This file provides guidance to AI Coding Agents when working with code in this repository.

## Project Overview

`jsonschema-markdown` converts JSON Schema files into readable Markdown documentation. It works as both a CLI tool (`jsonschema-markdown`) and a Python library (`jsonschema_markdown.generate()`). Uses CalVer (YYYY.MM.MICRO) versioning.

## Commands

```bash
# Install dependencies
uv sync --all-extras --dev

# Run all tests
uv run pytest -v

# Run a single test file
uv run pytest tests/test_generate.py -v

# Run a single test by name
uv run pytest -k "test_generate_custom_title" -v

# Lint and format
uv run ruff check .
uv run ruff format .
uv run ruff format --diff .   # check only

# Regenerate expected test outputs (run after changing converter logic)
uv run ./scripts/generate-tests.sh
```

## Adding Test Schemas

When adding a new test schema under `tests/schema-examples/`, **do not create expected `.md` files manually**. Run `uv run ./scripts/generate-tests.sh` to generate all expected outputs consistently. This also catches regressions in other schemas.

## Architecture

The package has three source files:

- **`jsonschema_markdown/converter/markdown.py`** — Core logic. The `generate()` function is the public API entry point. It processes a JSON schema dict and produces a Markdown string with tables for properties. Key internal functions:
  - `_create_definition_table()` — Builds the Markdown table for a schema's properties
  - `_process_properties_recursively()` — Walks nested objects/arrays using dot notation (e.g., `parent.child[].prop`)
  - `_get_property_details()` — Resolves property types, `$ref`, enums, patterns, ranges, combinators (`oneOf`/`anyOf`/`allOf`)
  - `_handle_array_like_property()` — Handles combinator types
  - `_extract_all_conditionals()` / `_process_conditionals()` — Handles `if`/`then`/`else` schemas
- **`jsonschema_markdown/utils.py`** — Small helpers: `sort_properties()` (required first, deprecated last), `create_enum_markdown()`, `create_const_markdown()`
- **`jsonschema_markdown/main.py`** — Click CLI that wraps `generate()`

## Testing

Tests use snapshot-style comparison: JSON schema files in `tests/schema-examples/` are converted and compared against corresponding `.md` files. The `test_schema_examples.py` parametrize test auto-discovers all `.json` files in that directory and matches them to `.md` (and optionally `_no-empty-columns.md`) files.

`tests/model.py` defines a Pydantic `Car` model used for integration tests in `test_generate.py`.

## Code Style

- Formatter/linter: **ruff** (always run `uv run ruff format` before committing)
- Ignored lint rules: E501 (line length), B008, B006
- Extended rules: B, C4, PIE, T20, SIM, TCH
- Tests are exempted from T201, PIE804, SIM115
