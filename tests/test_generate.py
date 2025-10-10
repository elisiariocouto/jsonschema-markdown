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


def test_generate_yaml_format_with_sort_keys():
    schema = {
        "title": "TestSchema",
        "type": "object",
        "description": "Test schema with examples",
        "examples": [
            {"z_field": "last", "a_field": "first", "m_field": "middle"}
        ],
        "properties": {"field": {"type": "string"}},
    }
    markdown = generate(schema, examples_format="yaml", sort_yaml_keys=True)

    a_pos = markdown.index("a_field")
    m_pos = markdown.index("m_field")
    z_pos = markdown.index("z_field")
    assert "a_field: first" in markdown
    assert "m_field: middle" in markdown
    assert "z_field: last" in markdown
    assert a_pos < m_pos < z_pos


def test_generate_yaml_format_without_sort_keys():
    schema = {
        "title": "TestSchema",
        "type": "object",
        "description": "Test schema with examples",
        "examples": [
            {"z_field": "last", "a_field": "first", "m_field": "middle"}
        ],
        "properties": {"field": {"type": "string"}},
    }
    markdown = generate(
        schema, examples_format="yaml", sort_yaml_keys=False
    )

    z_pos = markdown.index("z_field")
    a_pos = markdown.index("a_field")
    m_pos = markdown.index("m_field")
    assert "a_field: first" in markdown
    assert "m_field: middle" in markdown
    assert "z_field: last" in markdown
    assert z_pos < a_pos < m_pos


def test_generate_yaml_format_default_preserves_order():
    schema = {
        "title": "TestSchema",
        "type": "object",
        "description": "Test schema with examples",
        "examples": [
            {"z_field": "last", "a_field": "first"}
        ],
        "properties": {"field": {"type": "string"}},
    }
    markdown = generate(schema, examples_format="yaml")
    z_pos = markdown.index("z_field")
    a_pos = markdown.index("a_field")
    assert z_pos < a_pos
