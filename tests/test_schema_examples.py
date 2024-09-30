import json
import os

import pytest

import jsonschema_markdown

SCHEMA_EXAMPLES_DIR = "tests/schema-examples"


def get_test_cases():
    test_cases = []
    for filename in os.listdir(SCHEMA_EXAMPLES_DIR):
        if filename.endswith(".json"):
            json_path = os.path.join(SCHEMA_EXAMPLES_DIR, filename)
            md_path = os.path.join(
                SCHEMA_EXAMPLES_DIR, filename.replace(".json", ".md")
            )
            md_no_empty_columns_path = os.path.join(
                SCHEMA_EXAMPLES_DIR, filename.replace(".json", "_no-empty-columns.md")
            )
            test_cases.append((json_path, md_path, {}))
            test_cases.append(
                (json_path, md_no_empty_columns_path, {"hide_empty_columns": True})
            )
    return test_cases


@pytest.mark.parametrize("json_path, md_path, kwargs", get_test_cases())
def test_schema_examples(json_path, md_path, kwargs):
    with open(json_path, "r") as f:
        schema = json.load(f)

    with open(md_path, "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema, **kwargs)
    assert markdown == expected_markdown
