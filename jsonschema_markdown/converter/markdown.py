import contextlib
import json
import sys
import urllib.parse

import yaml
from loguru import logger

from jsonschema_markdown.utils import (
    create_const_markdown,
    create_enum_markdown,
    sort_properties,
)


def _should_include_column(column_values):
    """
    Check if any item has a non-falsy (non-empty) value for this column.
    """
    return any(value for value in column_values)


def _format_example(example, examples_format):
    """
    Format the example based on the examples_format. Only works for dict.
    """

    try:
        if examples_format == "yaml":
            if isinstance(example, dict):
                return f"```yaml\n{yaml.dump(example)}\n```"
            else:
                return f"```yaml\n{example}\n```"
        elif examples_format == "json":
            if isinstance(example, dict):
                return f"```json\n{json.dumps(example, indent=2)}\n```"
            else:
                return f"```json\n{example}\n```"
    except Exception:
        logger.debug(f"Failed to format example in '{examples_format}': {example}")

    return f"```\n{example}\n```"


def _get_schema_header(
    schema: dict,
    ref_key: str,
    description_fallback: str,
    nested: bool = False,
    examples_format: str = "text",
) -> str:
    """
    Get the title and description of the schema.

    If nested, all headings are increased by one level.
    """

    prefix = "" if not nested else "#"

    md = ""
    title = schema.get("title", ref_key) if not nested else ref_key
    # Add the title and description of the schema
    md += f"{prefix}# {title}\n\n"
    description = schema.get("description", description_fallback).strip(" \n")
    md += description if description else description_fallback
    md += "\n\n"

    # Add examples if present
    examples = schema.get("examples", [])
    if examples:
        md += f"{prefix}### Examples\n\n"
        for example in examples:
            md += _format_example(example, examples_format)
            md += "\n\n"

    md += f"{prefix}### Type: `{schema.get('type', 'object(?)').strip()}`\n\n"

    return md


def generate(
    schema: dict,
    title: str = "jsonschema-markdown",
    footer: bool = True,
    replace_refs: bool = False,
    debug: bool = False,
    hide_empty_columns: bool = False,
    examples_format: str = "text",
) -> str:
    """
    Generate a markdown string from a given JSON schema.

    Args:
        schema: The JSON schema to generate markdown from.
        title: The title of the markdown document.
        footer: Whether to include a footer section in the markdown with the current date and time.
        replace_refs: This feature is experimental. Whether to replace JSON references with their resolved values.
        debug: Whether to print debug messages.

    Returns:
        str: The generated markdown string.
    """
    # Set the log level
    if debug:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if replace_refs:
        import jsonref

        _schema: dict = jsonref.replace_refs(schema)  # type: ignore
    else:
        _schema = schema
    markdown = ""

    # Add the title and description of the schema
    markdown += _get_schema_header(
        _schema,
        title,
        "JSON Schema missing a description, provide it using the `description` key in the root of the JSON document.",
        examples_format=examples_format,
    )

    defs = _schema.get("definitions", _schema.get("$defs", {}))
    markdown += _create_definition_table(
        _schema, defs, hide_empty_columns=hide_empty_columns
    )

    if defs:
        markdown += "\n---\n\n# Definitions\n\n"
        for key, definition in defs.items():
            markdown += _get_schema_header(
                definition,
                key,
                "No description provided for this model.",
                nested=True,
                examples_format=examples_format,
            )
            markdown += _create_definition_table(
                definition, defs, hide_empty_columns=hide_empty_columns
            )

    if footer:
        # Add timestamp and a link to the project
        markdown += "\n---\n\nMarkdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown)."

    res = markdown.strip(" \n")
    res += "\n"

    return res


def _create_definition_table(schema: dict, defs: dict, hide_empty_columns: bool) -> str:
    """
    Create a table of the properties in the schema.

    Returns: Markdown table with the following columns
    - Property name
    - Type
    - Required
    - Possible Values / Definition Subschema
    - Deprecated
    - Default value
    - Description
    - Examples

    Search for deprecated string in the description or a deprecated key set to true in the property
    """

    logger.debug(f"Creating definition table for schema: {schema}")

    if schema.get("enum"):
        logger.debug("Creating enum markdown")
        return create_enum_markdown(schema)

    if schema.get("const"):
        logger.debug("Creating const markdown")
        return create_const_markdown(schema)

    markdown = ""

    # Add a warning before the table to indicate if additional properties are allowed
    if not schema.get("additionalProperties", True):
        markdown += "> ⚠️ Additional properties are not allowed.\n\n"

    if not schema.get("properties"):
        return markdown

    schema["properties"] = sort_properties(schema)

    table_items = []

    for property_name, property_details in schema["properties"].items():
        property_type = property_details.get("type")

        logger.debug(f"Processing {property_name} of type {property_type}")
        logger.debug(f"Property details: {property_details}")

        property_type, possible_values = _get_property_details(
            property_type, property_details, defs
        )

        logger.debug(
            f"Finished processing {property_name} of type {property_type}: {possible_values}"
        )

        default = property_details.get("default")
        description = property_details.get("description", "").strip(" \n")

        # Add backticks for each example, and join them with a comma and a space into a single string
        examples = ", ".join(
            [
                f"```{str(example)}```"
                for example in property_details.get("examples", [])
            ]
        )

        item = {
            "property": property_name,
            "type": property_type,
            "required": "✅" if property_name in schema.get("required", []) else "",
            "possible_values": possible_values,
            "deprecated": (
                "⛔️"
                if "[deprecated]"
                in str(property_details.get("description", "")).lower()
                or property_details.get("deprecated")
                else ""
            ),
            "default": "`" + json.dumps(default) + "`" if default else "",
            "description": description,
            "examples": examples,
        }
        table_items.append(item)

    # This should not happen, but just in case
    if not table_items:
        markdown += "No items to display."
        return markdown

    if hide_empty_columns:
        always_include_columns = ["property", "type", "required", "description"]
        # Determine which columns should be included
        columns = list(table_items[0].keys())
        include_column = {
            column: _should_include_column([item[column] for item in table_items])
            for column in columns
        }

        # Include the columns that should always be included
        for column in always_include_columns:
            include_column[column] = True

        # Generate the header row
        capitalized_columns = [
            col.replace("_", " ").capitalize() for col in columns if include_column[col]
        ]
        markdown += "| " + " | ".join(capitalized_columns) + " |\n"
        # Generate the separator row
        markdown += (
            "| "
            + " | ".join(["-" * len(col) for col in columns if include_column[col]])
            + " |\n"
        )

        # Generate the item rows
        for item in table_items:
            markdown += (
                "| "
                + " | ".join([str(item[col]) for col in columns if include_column[col]])
                + " |\n"
            )
    else:
        # Generate the header row
        capitalized_columns = [
            col.replace("_", " ").capitalize() for col in table_items[0]
        ]
        markdown += "| " + " | ".join(capitalized_columns) + " |\n"

        # Generate the separator row
        markdown += (
            "| " + " | ".join(["-" * len(col) for col in table_items[0]]) + " |\n"
        )
        # Generate the item rows

        for item in table_items:
            markdown += "| " + " | ".join(item.values()) + " |\n"

    return f"{markdown}\n"


def _get_property_ref(ref, defs):
    ref = ref.split("/")[-1]
    t = defs[ref].get("type")
    if ref in defs:
        return (
            f"`{t}`" if t else "Missing type",
            f"[{ref}](#{ref.replace(' ', '-').lower()})",
        )
    else:
        return "Missing type", "Missing definition"


def get_property_if_ref(property_details: dict, defs) -> tuple:
    """
    Check if the property is a reference.
    """

    # Check if the property is a reference
    ref_from_property = property_details.get("$ref")
    if ref_from_property:
        return _get_property_ref(ref_from_property, defs)

    # Check if the property is a reference in additionalProperties
    ref_from_additional_properties = (
        property_details["additionalProperties"].get("$ref")
        if isinstance(property_details.get("additionalProperties"), dict)
        else None
    )
    if ref_from_additional_properties:
        return _get_property_ref(ref_from_additional_properties, defs)

    return None, None


def _handle_array_like_property(
    property_type: str, property_details: dict, defs: dict, is_array=False
):
    """
    Handle properties that are array-like.
    """
    # TODO: Refactor this function to be more readable, handle arrays in a separate function

    array_type = (
        "oneOf"
        if "oneOf" in property_details
        else (
            "anyOf"
            if "anyOf" in property_details
            else "allOf"
            if "allOf" in property_details
            else None
        )
    )

    if array_type is None:
        logger.warning(
            f"Array-like property without oneOf, anyOf or allOf: {property_type} {property_details}"
        )
        # TODO: Support for items, prefixItems, contains, minContains, maxContains, uniqueItems, unevaluatedItems
        # https://json-schema.org/understanding-json-schema/reference/array
        return f"`{property_type}`", {}

    array_separator = {"oneOf": " or ", "anyOf": " and/or ", "allOf": " and "}

    removed_null = False
    with contextlib.suppress(Exception):
        property_details[array_type].remove({"type": "null"})
        removed_null = True

    types = []
    details = []

    for value in property_details[array_type]:
        ref_type, ref_details = get_property_if_ref(value, defs)
        if ref_type or ref_details:
            types.append(ref_type)
            details.append(ref_details)
        else:
            ref_type, ref_details = _get_property_details(
                value.get("type"), value, defs
            )
            types.append(ref_type)
            details.append(ref_details)

    # FIXME: Hacky way to handle arrays with null values
    return_type = None
    if is_array:
        return_type = "`array`"
        if removed_null:
            return_type = "`array` or `null`"
    else:
        if removed_null:
            types.append("`null`")

    # Arrays should return the type as array
    # Other array-like properties should return the types of the nested oneOf, anyOf or allOf
    if return_type:
        return return_type, array_separator[array_type].join(sorted(details))
    else:
        # Dedeuplicate list of types, join them with null at the end if present
        types = sorted(set(types))
        if "`null`" in types:
            types.remove("`null`")
            types.append("`null`")
        return " or ".join(types), array_separator[array_type].join(sorted(details))


def _get_property_details(
    property_type: str, property_details: dict, defs: dict
) -> tuple[str, str]:
    """
    Get the possible values for a property.
    """

    # Check if the property is a reference
    ref_type, ref_details = get_property_if_ref(property_details, defs)
    if ref_type or ref_details:
        return ref_type, ref_details

    if "additionalProperties" in property_details and not isinstance(
        property_details["additionalProperties"], bool
    ):
        logger.warning(
            f"Additional properties not a boolean: {property_details['additionalProperties']}"
        )
        # new_type = property_details["additionalProperties"].get("type")
        # return new_type, new_type

    if "enum" in property_details:
        return (
            f"`{property_type}`",
            " ".join([f"`{str(value)}`" for value in property_details["enum"]]),
        )

    # Handle array-like properties
    if any(key in property_details for key in ["oneOf", "anyOf", "allOf"]):
        t, d = _handle_array_like_property(property_type, property_details, defs)
        if t and d:
            return t, d

    if property_details.get("items") == {}:
        return f"`{property_type}`", "Any type"

    if "items" in property_details:
        if any(key in property_details["items"] for key in ["oneOf", "anyOf", "allOf"]):
            t, d = _handle_array_like_property(
                property_type, property_details["items"], defs, is_array=True
            )
            if t and d:
                return t, d

        ref_type, ref_details = get_property_if_ref(property_details["items"], defs)
        if ref_type or ref_details:
            return f"`{property_type}`", ref_details
        else:
            ref_type, ref_details = _get_property_details(
                property_details["items"].get("type"), property_details["items"], defs
            )
            return f"`{property_type}`", ref_details

    elif "pattern" in property_details:
        pattern = property_details["pattern"]
        res_details = f"[`{pattern}`](https://regex101.com/?regex={urllib.parse.quote_plus(pattern)})"
        return f"`{property_type}`", res_details
    elif "const" in property_details:
        res_details = f"`{property_details.get('const')}`"
        return "`const`", res_details
    elif property_type in ["integer", "number"]:
        # write the range of the integer in the format a <= x <= b
        minimum = property_details.get("minimum")
        maximum = property_details.get("maximum")
        exclusive_minimum = property_details.get("exclusiveMinimum")
        exclusive_maximum = property_details.get("exclusiveMaximum")

        min_details = ""
        max_details = ""
        res_details = ""

        if minimum is not None:
            min_details += f"{minimum} <="
        elif exclusive_minimum is not None:
            min_details += f"{exclusive_minimum} <"

        if maximum is not None:
            max_details += f"<= {maximum}"
        elif exclusive_maximum is not None:
            max_details += f"< {exclusive_maximum}"

        if min_details == "" and max_details == "":
            # fallback to original property_type when no range is specified
            res_details = property_type
        else:
            res_details = f"`{min_details} x {max_details}`"

        # check if multipleOf is present
        multiple_of = property_details.get("multipleOf")
        if multiple_of:
            res_details += f" and multiple of `{multiple_of}`"

        return f"`{property_type}`", res_details
    elif property_details.get("type") == "string":
        _format = property_details.get("format")
        _max_length = property_details.get("maxLength")
        _min_length = property_details.get("minLength")
        if _format:
            return (
                f"`{property_type}`",
                f"Format: [`{_format}`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats)",
            )
        elif _max_length or _min_length:
            if _max_length and _min_length:
                return (
                    f"`{property_type}`",
                    f"Length: `{_min_length} <= string <= {_max_length}`",
                )
            elif _max_length:
                return f"`{property_type}`", f"Length: `string <= {_max_length}`"
            elif _min_length:
                return f"`{property_type}`", f"Length: `string >= {_min_length}`"
            else:
                return f"`{property_type}`", property_type
        else:
            return f"`{property_type}`", property_type
    else:
        return f"`{property_type}`", property_type
