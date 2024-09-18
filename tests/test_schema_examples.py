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


def test_basic_anyof_multiple_types():
    with open("tests/schema-examples/basic-anyOf-multiple-types.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/basic-anyOf-multiple-types.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema)

    assert markdown == expected_markdown


def test_basic_anyof_multiple_types_empty_columns():
    with open("tests/schema-examples/basic-anyOf-multiple-types.json", "r") as f:
        schema = json.load(f)

    with open(
        "tests/schema-examples/basic-anyOf-multiple-types_no-empty-columns.md", "r"
    ) as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema, hide_empty_columns=True)

    assert markdown == expected_markdown


def test_basic_anyof_null():
    with open("tests/schema-examples/basic-anyOf-multiple-types.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/basic-anyOf-multiple-types.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema)

    assert markdown == expected_markdown


def test_basic_anyof_null_empty_columns():
    with open("tests/schema-examples/basic-anyOf-null.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/basic-anyOf-null_no-empty-columns.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema, hide_empty_columns=True)

    assert markdown == expected_markdown
