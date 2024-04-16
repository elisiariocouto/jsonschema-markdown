from jsonschema_markdown import generate
from tests.model import Car


def test_generate():
    schema = Car.model_json_schema()
    markdown = generate(schema)

    with open("tests/model.md", "r") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown


def test_generate_hide_empty_columns():
    schema = Car.model_json_schema()
    markdown = generate(schema, hide_empty_columns=True)

    with open("tests/model_no-empty-columns.md", "r") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown


def test_generate_custom_title_no_footer():
    schema = Car.model_json_schema()
    markdown = generate(schema, title="Car (custom title)", footer=False)

    with open("tests/model_custom-title_no-footer.md", "r") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown
