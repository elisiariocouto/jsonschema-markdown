# jsonschema-markdown

Generate markdown documentation from JSON Schema files. The main goal is to generate
documentation that is easy to read and understand.

Can be used as a command line tool or as a library.

## Installation

```bash
pipx install jsonschema-markdown
```

## Usage

To use `jsonschema-markdown` as a CLI, just pass the filename as an argument and redirect
the output to a file.

```bash
$ jsonschema-markdown --help
Usage: jsonschema-markdown [OPTIONS] FILENAME

  Load FILENAME and output a markdown version.

  Use '-' as FILENAME to read from stdin.

Options:
  -t, --title TEXT          Do not use the title from the schema, use this
                            title instead.
  --footer / --no-footer    Add a footer with a link to the project.
                            [default: footer]
  --resolve / --no-resolve  [Experimental] Resolve $ref pointers.  [default:
                            no-resolve]
  --debug / --no-debug      Enable debug output.  [default: no-debug]
  --version                 Show the version and exit.
  --help                    Show this message and exit.

# Example
$ jsonschema-markdown schema.json > schema.md
```

## Usage with Docker
The `jsonschema-markdown` command is also available as a Docker image. To use it, you can mount the schema file as a volume.

```bash
cat my-schema.json | docker run --rm -i elisiariocouto/jsonschema-markdown - > schema.md
```
⚠️ **Warning**: Do not pass the `-t` flag.

The Docker image is available at:
 - [elisiariocouto/jsonschema-markdown](https://hub.docker.com/r/elisiariocouto/jsonschema-markdown)
 - [ghcr.io/elisiariocouto/jsonschema-markdown](https://ghcr.io/elisiariocouto/jsonschema-markdown)

## Usage as a library

To use it as a library, load your JSON schema file as Python `dict` and pass it to generate.
The function will return a string with the markdown.

```python
import jsonschema_markdown

with open('schema.json') as f:
    schema = json.load(f)

markdown = jsonschema_markdown.generate(schema)
```

## Features

Partially inspired by [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans),
this project does not currently support all features of JSON Schema, but it should support:

  - Required fields
  - String patterns
  - Enumerations
  - Default values
  - Descriptions and titles
  - Nested objects
  - Basic OneOf, AnyOf, AllOf functionality
  - Arrays
  - Integers with minimum, maximum values and exclusives
  - Boolean values
  - Deprecation notices (searches for case-insensitive `deprecated` in the field description)

## Caveats
  - This project is still in early development, and the output may change in the future.
  - Custom definitions are expected to be in the same file as the schema that uses them,
    in the `definitions` or `$defs` parameter at the root of the document.
