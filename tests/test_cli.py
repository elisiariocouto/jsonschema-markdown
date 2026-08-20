import builtins

from click.testing import CliRunner

from jsonschema_markdown.main import cli

UNICODE_SCHEMA = "tests/schema-examples/unicode-content.json"


def test_cli_reads_unicode_file():
    result = CliRunner().invoke(cli, [UNICODE_SCHEMA])

    assert result.exit_code == 0
    assert "Café Menu — Spécialités" in result.output
    assert "日本語の説明" in result.output


def test_cli_reads_unicode_stdin():
    with open(UNICODE_SCHEMA, "r", encoding="utf-8") as f:
        schema = f.read()

    result = CliRunner().invoke(cli, ["-"], input=schema)

    assert result.exit_code == 0
    assert "Café Menu — Spécialités" in result.output


def test_cli_reads_unicode_with_non_utf8_locale(monkeypatch):
    """The CLI must not depend on the platform's default encoding.

    Emulates Windows, where locale.getpreferredencoding() is typically cp1252 and
    an implicit text-mode open() would raise UnicodeDecodeError on a UTF-8 schema.
    """
    original_open = builtins.open

    def cp1252_default_open(*args, **kwargs):
        mode = kwargs.get("mode", args[1] if len(args) > 1 else "r")
        if "b" not in mode and not kwargs.get("encoding"):
            kwargs["encoding"] = "cp1252"
        return original_open(*args, **kwargs)

    monkeypatch.setattr(builtins, "open", cp1252_default_open)

    result = CliRunner().invoke(cli, [UNICODE_SCHEMA])

    assert result.exit_code == 0, result.exception
    assert "Café Menu — Spécialités" in result.output
