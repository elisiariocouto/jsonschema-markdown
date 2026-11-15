from jsonschema_markdown import generate
from tests.model import Car


def test_generate():
    schema = Car.model_json_schema()
    markdown = generate(schema)

    with open("tests/model.md", "r", encoding="utf-8") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown


def test_generate_hide_empty_columns():
    schema = Car.model_json_schema()
    markdown = generate(schema, hide_empty_columns=True)

    with open("tests/model_no-empty-columns.md", "r", encoding="utf-8") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown


def test_generate_custom_title_no_footer():
    schema = Car.model_json_schema()
    markdown = generate(schema, title="Car (custom title)", footer=False)

    with open("tests/model_custom-title_no-footer.md", "r", encoding="utf-8") as f:
        expected_markdown = f.read()

    assert markdown == expected_markdown


def test_generate_yaml_format_with_sort_keys():
    schema = {
        "title": "TestSchema",
        "type": "object",
        "description": "Test schema with examples",
        "examples": [{"z_field": "last", "a_field": "first", "m_field": "middle"}],
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
        "examples": [{"z_field": "last", "a_field": "first", "m_field": "middle"}],
        "properties": {"field": {"type": "string"}},
    }
    markdown = generate(schema, examples_format="yaml", sort_yaml_keys=False)

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
        "examples": [{"z_field": "last", "a_field": "first"}],
        "properties": {"field": {"type": "string"}},
    }
    markdown = generate(schema, examples_format="yaml")
    z_pos = markdown.index("z_field")
    a_pos = markdown.index("a_field")
    assert z_pos < a_pos


def test_generate_resolved_refs_keep_null_in_every_property():
    """Rendering a schema shared via resolved $refs must not lose its null option.

    With replace_refs, properties that reference the same definition share one
    dict, so detecting null by modifying it dropped null from all but the first.
    """
    schema = {
        "title": "Shared",
        "type": "object",
        "properties": {
            "first_list": {"type": "array", "items": {"$ref": "#/$defs/MaybeStr"}},
            "second_list": {"type": "array", "items": {"$ref": "#/$defs/MaybeStr"}},
            "first_value": {"$ref": "#/$defs/MaybeStr"},
            "second_value": {"$ref": "#/$defs/MaybeStr"},
        },
        "$defs": {"MaybeStr": {"anyOf": [{"type": "string"}, {"type": "null"}]}},
    }
    markdown = generate(schema, replace_refs=True, hide_empty_columns=True)

    assert "| first_list | `array` |  | string or null |" in markdown
    assert "| second_list | `array` |  | string or null |" in markdown
    assert "| first_value | `string` or `null` |" in markdown
    assert "| second_value | `string` or `null` |" in markdown


def _table_row(markdown: str, prop: str) -> str:
    return next(
        line for line in markdown.splitlines() if line.startswith(f"| {prop} |")
    )


def test_generate_nullable_property_with_untyped_alternatives_lists_null_once():
    """The property's own nullable type adds null; the anyOf must not add it again."""
    schema = {
        "title": "T",
        "type": "object",
        "properties": {
            "p": {
                "type": ["string", "null"],
                "anyOf": [{"pattern": "^a"}, {"pattern": "^b"}],
            }
        },
    }
    row = _table_row(generate(schema, hide_empty_columns=True), "p")

    assert row.count("`null`") == 1


def test_generate_one_of_with_any_value_entry_is_not_any_type():
    """In a oneOf, values matching the always-matching entry and another are rejected."""
    schema = {
        "title": "T",
        "type": "object",
        "properties": {
            "p": {"type": "array", "items": {"oneOf": [{}, {"type": "string"}]}}
        },
    }
    row = _table_row(generate(schema, hide_empty_columns=True), "p")

    assert "Any type" not in row
