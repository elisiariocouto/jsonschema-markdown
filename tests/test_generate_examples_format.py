import pytest

from jsonschema_markdown.converter.markdown import _format_example


@pytest.mark.parametrize(
    "example, format_type, expected_md",
    [
        ({"key": "value"}, "yaml", "```yaml\nkey: value\n\n```"),
        ("example string", "yaml", "```yaml\nexample string\n```"),
        ({"key": "value"}, "json", '```json\n{\n  "key": "value"\n}\n```'),
        ("example string", "json", "```json\nexample string\n```"),
        ({"key": "value"}, "text", "```\n{'key': 'value'}\n```"),
        ({"key": "value"}, "invalid_format", "```\n{'key': 'value'}\n```"),
    ],
)
def test_generate_examples_format(example, format_type, expected_md):
    formatted = _format_example(example, format_type)
    assert formatted == expected_md


@pytest.mark.parametrize(
    "example, sort_yaml_keys, expected_md",
    [
        # Test sorted keys (default behavior)
        (
            {"z_key": "value1", "a_key": "value2", "m_key": "value3"},
            True,
            "```yaml\na_key: value2\nm_key: value3\nz_key: value1\n\n```",
        ),
        # Test unsorted keys (preserves order)
        (
            {"z_key": "value1", "a_key": "value2", "m_key": "value3"},
            False,
            "```yaml\nz_key: value1\na_key: value2\nm_key: value3\n\n```",
        ),
        # Test nested dict with sorted keys
        (
            {
                "outer_z": {"inner_z": 1, "inner_a": 2},
                "outer_a": "value",
            },
            True,
            "```yaml\nouter_a: value\n"
            "outer_z:\n  inner_a: 2\n  inner_z: 1\n\n```",
        ),
        # Test nested dict with unsorted keys (preserves order)
        (
            {
                "outer_z": {"inner_z": 1, "inner_a": 2},
                "outer_a": "value",
            },
            False,
            "```yaml\nouter_z:\n  inner_z: 1\n  inner_a: 2\n"
            "outer_a: value\n\n```",
        ),
    ],
)
def test_yaml_sort_keys(example, sort_yaml_keys, expected_md):
    formatted = _format_example(example, "yaml", sort_yaml_keys)
    assert formatted == expected_md


def test_sort_yaml_keys_default_false():
    """Test that the default value for sort_yaml_keys is False."""
    example = {"z_key": "value1", "a_key": "value2"}
    formatted = _format_example(example, "yaml")
    # Should preserve insertion order (z before a)
    expected = "```yaml\nz_key: value1\na_key: value2\n\n```"
    assert formatted == expected


def test_sort_yaml_keys_only_affects_yaml():
    """Test that sort_yaml_keys parameter does not affect json or text."""
    example = {"z_key": "value1", "a_key": "value2"}
    # JSON should maintain dict order regardless of sort_yaml_keys
    json_result = _format_example(example, "json", sort_yaml_keys=False)
    # JSON uses json.dumps which doesn't sort by default in Python 3.7+
    assert "z_key" in json_result and "a_key" in json_result
    # Text format should be unaffected
    text_result = _format_example(example, "text", sort_yaml_keys=False)
    assert "```\n{" in text_result
