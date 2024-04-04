import json

import jsonschema_markdown


def test_integer():
    with open("tests/schema-examples/integer/integer.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/integer/integer.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema, footer=False)

    assert markdown == expected_markdown


def test_simple():
    with open("tests/schema-examples/simple/simple.json", "r") as f:
        schema = json.load(f)

    with open("tests/schema-examples/simple/simple.md", "r") as f:
        expected_markdown = f.read()

    markdown = jsonschema_markdown.generate(schema)

    assert markdown == expected_markdown
