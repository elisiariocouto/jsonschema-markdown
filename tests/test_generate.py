from jsonschema_markdown import generate
from tests.model import Car


def test_generate():
    schema = Car.model_json_schema()
    markdown = generate(schema)

    with open("tests/model.md", "r") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown
