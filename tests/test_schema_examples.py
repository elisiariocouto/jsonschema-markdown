import json

import jsonschema_markdown


def test_integer():
    with open("tests/schema-examples/integer.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/integer.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema)

    assert markdown == expected_markdown


def test_integer_hide_empty_columns():
    with open("tests/schema-examples/integer.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/integer_no-empty-columns.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema, hide_empty_columns=True)

    assert markdown == expected_markdown


def test_simple():
    with open("tests/schema-examples/simple.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/simple.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema)

    assert markdown == expected_markdown


def test_simple_hide_empty_columns():
    with open("tests/schema-examples/simple.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/simple_no-empty-columns.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema, hide_empty_columns=True)

    assert markdown == expected_markdown
