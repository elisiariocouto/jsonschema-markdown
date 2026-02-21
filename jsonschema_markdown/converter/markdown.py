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


def _format_example(example, examples_format, sort_yaml_keys=False):
    """
    Format the example based on the examples_format. Only works for dict.
    """

    try:
        if examples_format == "yaml":
            if isinstance(example, dict):
                return f"```yaml\n{yaml.dump(example, sort_keys=sort_yaml_keys).strip()}\n```"
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
    sort_yaml_keys: bool = False,
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
            md += _format_example(example, examples_format, sort_yaml_keys)
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
    sort_yaml_keys: bool = False,
) -> str:
    """
    Generate a markdown string from a given JSON schema.

    Args:
        schema: The JSON schema to generate markdown from.
        title: The title of the markdown document.
        footer: Whether to include a footer section in the markdown with the current date and time.
        replace_refs: This feature is experimental. Whether to replace JSON references with their resolved values.
        debug: Whether to print debug messages.
        hide_empty_columns: Whether to hide empty columns in the output.
        examples_format: Format of the examples in the output (text, yaml, json).
        sort_yaml_keys: Whether to sort keys when formatting YAML examples.

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
        sort_yaml_keys=sort_yaml_keys,
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
                sort_yaml_keys=sort_yaml_keys,
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


def _process_properties_recursively(
    properties: dict,
    property_path: str,
    required_props: list,
    defs: dict,
    conditional_properties: dict = {},
) -> list:
    """
    Recursively process schema properties, including nested objects and arrays.

    Args:
        properties: Dictionary of properties to process
        property_path: Current property path (for nested notation)
        required_props: List of required properties at current level
        defs: Definitions dictionary
        conditional_properties: Dict mapping property names to conditional variants

    Returns:
        List of property items for markdown table
    """
    table_items = []

    for prop_name, prop_details in properties.items():
        # Build the full property path using dot notation
        full_path = f"{property_path}.{prop_name}" if property_path else prop_name

        prop_type = prop_details.get("type")
        logger.debug(f"Processing {full_path} of type {prop_type}")

        # Process the current property
        property_type, possible_values = _get_property_details(
            prop_type, prop_details, defs
        )

        has_default_value = "default" in prop_details
        default_value = (
            "`" + json.dumps(prop_details.get("default")) + "`"
            if has_default_value
            else ""
        )
        description = prop_details.get("description", "").strip(" \n")

        # Replace newlines in description with <br /> for markdown to prevent table breaking
        if "\n" in description:
            description = description.replace("\n", "<br />")

        examples = ", ".join(
            [f"```{str(example)}```" for example in prop_details.get("examples", [])]
        )

        # Add the current property to our results
        item = {
            "property": full_path,
            "type": property_type,
            "required": "✅" if prop_name in required_props else "",
            "possible_values": possible_values,
            "conditional": "" if conditional_properties else "",
            "deprecated": (
                "⛔️"
                if "[deprecated]" in str(prop_details.get("description", "")).lower()
                or prop_details.get("deprecated")
                else ""
            ),
            "default": default_value,
            "description": description,
            "examples": examples,
        }

        # Remove conditional key if there are no conditionals to keep consistent dict keys
        if not conditional_properties:
            del item["conditional"]

        table_items.append(item)

        # Add conditional variants if they exist
        if full_path in conditional_properties:
            for conditional_variant in conditional_properties[full_path]:
                conditional_item = {
                    "property": full_path,
                    "type": conditional_variant["type"],
                    "required": "✅" if conditional_variant.get("required") else "",
                    "possible_values": conditional_variant["possible_values"],
                    "conditional": conditional_variant["condition"],
                    "deprecated": "",
                    "default": "",
                    "description": "",
                    "examples": "",
                }
                table_items.append(conditional_item)

        # If this is an object with properties, process its nested properties
        if prop_type == "object" and prop_details.get("properties"):
            nested_items = _process_properties_recursively(
                prop_details["properties"],
                full_path,
                prop_details.get("required", []),
                defs,
                conditional_properties,
            )
            table_items.extend(nested_items)

        # If this is an array with items that are objects, process them too
        elif prop_type == "array" and isinstance(prop_details.get("items"), dict):
            items_schema = prop_details["items"]
            if items_schema.get("type") == "object" and items_schema.get("properties"):
                array_path = f"{full_path}[]"  # Add [] to indicate array items
                _combinator_key = (
                    "oneOf"
                    if "oneOf" in items_schema
                    else (
                        "anyOf"
                        if "anyOf" in items_schema
                        else "allOf"
                        if "allOf" in items_schema
                        else None
                    )
                )
                _separator = {"oneOf": " or ", "anyOf": " and/or ", "allOf": " and "}
                if _combinator_key is not None and all(
                    _is_constraint_only(e) for e in items_schema[_combinator_key]
                ):
                    # The combinator entries are pure constraints (e.g. required only),
                    # not type alternatives. Emit a single combined row for all properties.
                    combined_name = _separator[_combinator_key].join(
                        f"{array_path}.{p}" for p in items_schema["properties"]
                    )
                    first_prop = next(iter(items_schema["properties"].values()))
                    p_type, p_values = _get_property_details(
                        first_prop.get("type"), first_prop, defs
                    )
                    combined_item = {
                        "property": combined_name,
                        "type": p_type,
                        "required": "",
                        "possible_values": p_values,
                        "deprecated": "",
                        "default": "",
                        "description": "",
                        "examples": "",
                    }
                    if conditional_properties:
                        combined_item["conditional"] = ""
                    table_items.append(combined_item)
                else:
                    nested_items = _process_properties_recursively(
                        items_schema["properties"],
                        array_path,
                        items_schema.get("required", []),
                        defs,
                        conditional_properties,
                    )
                    table_items.extend(nested_items)

    return table_items


def _extract_all_conditionals(schema: dict, defs: dict, prefix: str = "") -> dict:
    """
    Recursively extract and process conditionals from a schema and all nested objects.

    Args:
        schema: The JSON schema to extract conditionals from.
        defs: Definitions dictionary for resolving references.
        prefix: Current property path prefix for nested objects (e.g. "address").

    Returns:
        A dict mapping full property paths (e.g. "address.postal_code") to lists of
        conditional variant dictionaries, each containing condition, type,
        possible_values, and required status.
    """
    conditional_properties = {}

    # Extract conditionals at current level
    conditionals = _extract_conditionals(schema)
    if conditionals:
        processed = _process_conditionals(conditionals, defs)
        for prop_name, variants in processed.items():
            full_path = f"{prefix}.{prop_name}" if prefix else prop_name
            conditional_properties[full_path] = variants

    # Recurse into nested object properties
    properties = schema.get("properties", {})
    for prop_name, prop_details in properties.items():
        if isinstance(prop_details, dict) and prop_details.get("type") == "object":
            full_path = f"{prefix}.{prop_name}" if prefix else prop_name
            nested = _extract_all_conditionals(prop_details, defs, full_path)
            conditional_properties.update(nested)

    return conditional_properties


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

    # Use the sort_properties function to maintain the order
    sorted_properties = sort_properties(schema)

    # Extract and process conditionals from all levels (including nested objects)
    conditional_properties = _extract_all_conditionals(schema, defs)

    # Process properties recursively instead of just the top level
    table_items = _process_properties_recursively(
        sorted_properties,
        "",  # Start with empty path
        schema.get("required", []),
        defs,
        conditional_properties,
    )

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


_TYPE_INFO_KEYS = frozenset(
    {
        "type",
        "$ref",
        "properties",
        "anyOf",
        "oneOf",
        "allOf",
        "enum",
        "const",
        "items",
        "pattern",
        "format",
        "additionalProperties",
    }
)


def _is_constraint_only(schema_entry: dict) -> bool:
    """Return True if entry has only constraint keywords (e.g. required), no type info."""
    return not any(key in schema_entry for key in _TYPE_INFO_KEYS)


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
        if _is_constraint_only(value):
            continue
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
    non_null_details = sorted(d for d in details if d is not None)
    if return_type:
        return return_type, array_separator[array_type].join(non_null_details)
    else:
        # Dedeuplicate list of types, join them with null at the end if present
        types = sorted(set(types))
        if "`null`" in types:
            types.remove("`null`")
            types.append("`null`")
        return " or ".join(types), array_separator[array_type].join(non_null_details)


def _extract_conditionals(schema: dict) -> list:
    """
    Extract if/then/else structures from a schema.

    Returns a list of conditional blocks, each containing 'if', 'then', and optionally 'else'.
    """
    conditionals = []

    # Check for direct if/then/else at schema level
    if "if" in schema:
        if_block = schema["if"]
        then_block = schema.get("then", {})
        else_block = schema.get("else", {})

        # Per JSON Schema spec, we ignore if without then or else
        if then_block or else_block:
            conditionals.append(
                {"if": if_block, "then": then_block, "else": else_block}
            )

    # Check for conditionals within allOf
    all_of = schema.get("allOf", [])
    if isinstance(all_of, list):
        for item in all_of:
            if isinstance(item, dict) and "if" in item:
                if_block = item["if"]
                then_block = item.get("then", {})
                else_block = item.get("else", {})

                if then_block or else_block:
                    conditionals.append(
                        {"if": if_block, "then": then_block, "else": else_block}
                    )

    return conditionals


def _format_condition(if_schema: dict) -> str:
    """
    Convert an if schema into a human-readable condition string.

    Handles const, enum, type, minimum, maximum, pattern, and property constraints.
    """
    if not isinstance(if_schema, dict):
        return "Complex condition"

    conditions = []

    # Handle properties with constraints
    if "properties" in if_schema and isinstance(if_schema["properties"], dict):
        for prop_name, prop_schema in if_schema["properties"].items():
            if isinstance(prop_schema, dict):
                if "const" in prop_schema:
                    conditions.append(f"{prop_name} = {prop_schema['const']}")
                elif "enum" in prop_schema:
                    values = ", ".join(str(v) for v in prop_schema["enum"])
                    conditions.append(f"{prop_name} in [{values}]")
                elif "type" in prop_schema:
                    conditions.append(f"{prop_name} is {prop_schema['type']}")
                elif "minimum" in prop_schema:
                    conditions.append(f"{prop_name} >= {prop_schema['minimum']}")
                elif "maximum" in prop_schema:
                    conditions.append(f"{prop_name} <= {prop_schema['maximum']}")
                elif "pattern" in prop_schema:
                    conditions.append(f'{prop_name} matches "{prop_schema["pattern"]}"')

    # If we found conditions, format them
    if conditions:
        condition_str = " AND ".join(conditions)
        return f"**If** {condition_str}"

    return "Complex condition"


def _process_conditionals(conditionals: list, defs: dict) -> dict:
    """
    Process conditional schemas into property modifications.

    Returns a dict mapping property paths to lists of conditional variants.
    Each variant includes condition, type, possible_values, and required status.
    """
    conditional_properties = {}

    for conditional_block in conditionals:
        condition = _format_condition(conditional_block["if"])

        # Process 'then' schema
        then_schema = conditional_block.get("then", {})
        if isinstance(then_schema, dict) and "properties" in then_schema:
            for prop_name, prop_details in then_schema["properties"].items():
                prop_type = prop_details.get("type")
                property_type, possible_values = _get_property_details(
                    prop_type, prop_details, defs
                )

                if prop_name not in conditional_properties:
                    conditional_properties[prop_name] = []

                conditional_properties[prop_name].append(
                    {
                        "condition": condition,
                        "type": property_type,
                        "possible_values": possible_values,
                        "required": prop_name in then_schema.get("required", []),
                    }
                )

        # Process 'else' schema
        else_schema = conditional_block.get("else", {})
        if isinstance(else_schema, dict) and "properties" in else_schema:
            else_condition = _format_condition(conditional_block["if"])
            # Indicate it's the else branch
            else_condition = else_condition.replace("**If**", "**If NOT**")

            for prop_name, prop_details in else_schema["properties"].items():
                prop_type = prop_details.get("type")
                property_type, possible_values = _get_property_details(
                    prop_type, prop_details, defs
                )

                if prop_name not in conditional_properties:
                    conditional_properties[prop_name] = []

                conditional_properties[prop_name].append(
                    {
                        "condition": else_condition,
                        "type": property_type,
                        "possible_values": possible_values,
                        "required": prop_name in else_schema.get("required", []),
                    }
                )

    return conditional_properties


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
        # escape any pipe characters in the pattern string to prevent markdown table formatting issues
        md_table_safe = pattern.replace("|", r"\|")
        res_details = f"[`{md_table_safe}`](https://regex101.com/?regex={urllib.parse.quote_plus(pattern)})"
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
