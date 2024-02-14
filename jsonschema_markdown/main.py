import json

import click

import jsonschema_markdown


@click.command()
@click.argument("filename", type=click.File("r"))
@click.option(
    "--footer/--no-footer",
    is_flag=True,
    default=True,
    show_default=True,
    help="Add a footer with a link to the project.",
)
@click.option(
    "--resolve/--no-resolve",
    is_flag=True,
    default=False,
    show_default=True,
    help="[Experimental] Resolve $ref pointers.",
)
@click.option(
    "--debug/--no-debug",
    is_flag=True,
    default=False,
    show_default=True,
    help="Enable debug output.",
)
@click.version_option(package_name="jsonschema_markdown")
def cli(filename, footer, resolve, debug):
    """
    Load FILENAME and output a markdown version.

    Use '-' as FILENAME to read from stdin.
    """

    file_contents = json.loads(filename.read())

    # Convert the file contents to markdown
    markdown = jsonschema_markdown.generate(
        file_contents, footer=footer, replace_refs=resolve, debug=debug
    )

    # Output the markdown
    click.echo(markdown)
