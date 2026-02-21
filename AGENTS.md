# Agent Instructions

## Adding test schemas

When adding a new test schema under `tests/schema-examples/`, **do not create the expected markdown files manually**.
Instead, run the generation script so all expected outputs are produced consistently and regressions in other schemas are caught automatically:

```bash
uv run ./scripts/generate-tests.sh
```

## Code formatting

Always run `uv run ruff format` before committing any Python changes.
