import json

import click

import jsonschema_markdown


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.version_option(package_name="jsonschema_markdown")
def cli(filename):
    """
    Load a file and output the markdown.
    """
    with open(filename, "r") as f:
        file_contents = json.load(f)

    # Convert the file contents to markdown
    markdown = jsonschema_markdown.generate(file_contents)

    # Output the markdown
    click.echo(markdown)
