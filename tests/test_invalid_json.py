from click.testing import CliRunner

from jsonschema_markdown.main import cli


def test_cli_rejects_invalid_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")

    result = CliRunner().invoke(cli, [str(bad)])

    assert result.exit_code == 2
    assert "Invalid value" in result.output
    assert "invalid JSON" in result.output
