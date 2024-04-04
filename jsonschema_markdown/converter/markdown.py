import contextlib
import json
import sys
import urllib.parse

from loguru import logger

from jsonschema_markdown.utils import (
    create_const_markdown,
    create_enum_markdown,
    sort_properties,
)


def generate(
    schema: dict,
    title: str = "jsonschema-markdown",
    footer: bool = True,
    replace_refs: bool = False,
    debug: bool = False,
) -> str:
    """
    Generate a markdown string from a given JSON schema.

    Parameters:
        schema (dict): The JSON schema to generate markdown from.
        title (str, optional): The title of the markdown document. Defaults to "jsonschema-markdown".
        footer (bool, optional): Whether to include a footer section in the markdown with the current date and time. Defaults to True.
        replace_refs (bool, optional): This feature is experimental. Whether to replace JSON references with their resolved values. Defaults to False.
        debug (bool, optional): Whether to print debug messages. Defaults to False.

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
    markdown += f"# {_schema.get('title', title)}\n\n"
    description = _schema.get("description", "").strip(" \n")
    markdown += (
        f"{description}\n\n"
        if description
        else "JSON Schema missing a description, provide it using the `description` key in the root of the JSON document.\n\n"
    )

    # Add examples if present
    examples = _schema.get("examples", [])
    if examples:
        markdown += "## Schema Examples\n\n"
        for example in examples:
            markdown += f"```\n{example}\n```\n\n"

    defs = _schema.get("definitions", _schema.get("$defs", {}))
    markdown += _create_definition_table(_schema, defs)

    if defs:
        markdown += "\n\n---\n\n# Definitions\n\n"

        for key, definition in defs.items():
            examples = definition.get("examples", [])
            description = definition.get(
                "description", "No description provided for this model."
            ).strip(" \n")
            markdown += f"\n\n## {definition.get('title', key)}\n\n"
            markdown += f"{description}\n\n"
            if examples:
                markdown += "### Examples\n\n"
                for example in examples:
                    markdown += f"```\n{example}\n```\n\n"
            markdown += f"### Type: `{definition.get('type', 'object(?)').strip()}`\n\n"
            markdown += _create_definition_table(definition, defs)

    if footer:
        # Add timestamp and a link to the project
        markdown += "\n\n---\n\nMarkdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown)."

    res = markdown.strip(" \n")
    res += "\n"

    return res


def _create_definition_table(schema: dict, defs: dict) -> str:
    """
    Create a table of the properties in the schema.
    Outputs a markdown table with the following columns:
    - Property name
    - Type
    - Required
    - Possible Values / Definition Subschema
    - Deprecated
    - Default value
    - Description

    Search for deprecated string in the description or a deprecated key set to true in the property
    """

    logger.debug(f"Creating definition table for schema: {schema}")

    if schema.get("enum"):
        logger.debug("Creating enum markdown")
        return create_enum_markdown(schema)

    if schema.get("const"):
        logger.debug("Creating const markdown")
        return create_const_markdown(schema)

    if schema.get("properties"):
        schema["properties"] = sort_properties(schema)

    markdown = ""

    # Add a warning before the table to indicate if additional properties are allowed
    if not schema.get("additionalProperties", True):
        markdown += "> ⚠️ Additional properties are not allowed.\n\n"

    markdown += "| Property | Type | Required | Possible Values | Deprecated | Default | Description | Examples\n"
    markdown += "| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | --------\n"

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

        markdown += (
            f"| {property_name} | "
            f"`{property_type}` | "
            f"{'✅' if property_name in schema.get('required', []) else ''} | "
            f"{possible_values}| "
            f"{'⛔️' if '[deprecated]' in str(property_details.get('description','')).lower() or property_details.get('deprecated') else ''} | "
            f"{'`'+json.dumps(default)+'`' if default else ''} | "
            f"{description} |"
            f"{examples} |\n"
        )

    return markdown


def _get_property_ref(ref, defs):
    ref = ref.split("/")[-1]
    if ref in defs:
        return (
            defs[ref].get("type", "object(?)"),
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


def _handle_array_like_property(property_type: str, property_details: dict, defs: dict):
    """
    Handle properties that are array-like.
    """

    array_type = (
        "oneOf"
        if "oneOf" in property_details
        else (
            "anyOf"
            if "anyOf" in property_details
            else "allOf" if "allOf" in property_details else None
        )
    )

    if array_type is None:
        logger.warning(
            f"Array-like property without oneOf, anyOf or allOf: {property_type} {property_details}"
        )
        return property_type, {}

    array_separator = {"oneOf": " or ", "anyOf": " and/or ", "allOf": " and "}

    # TODO: We are removing the null type from the this property, some libraries add this
    # for nullable properties, we should find a better way to handle this
    removed_null = False
    with contextlib.suppress(Exception):
        property_details[array_type].remove({"type": "null"})
        removed_null = True
        if len(property_details[array_type]) == 1:
            return _get_property_details(
                property_details[array_type][0].get("type"),
                property_details[array_type][0],
                defs,
            )

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
    types_set = set(types)
    if len(types_set) > 1 and removed_null:
        logger.warning(
            f"Multiple types in items,{array_type} property: {types_set}. Selecting the first one.",
        )

    if removed_null:
        logger.debug(
            f"Removed null type from {property_type} property, got {types_set} as types, selecting the first one {types[0]}"
        )
        return types[0], array_separator[array_type].join(details)
    elif property_type is None:
        logger.warning(
            f"Array-like property without type, selecting first type of subschema: {types[0]}"
        )
        return types[0], array_separator[array_type].join(details)
    else:
        logger.debug(
            f"Array-like property without null type, selecting original type {property_type}"
        )
        return property_type, array_separator[array_type].join(details)


def _get_property_details(property_type: str, property_details: dict, defs: dict):
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
            property_type,
            " ".join([f"`{str(value)}`" for value in property_details["enum"]]),
        )

    # Handle array-like properties
    if any(key in property_details for key in ["oneOf", "anyOf", "allOf"]):
        t, d = _handle_array_like_property(property_type, property_details, defs)
        if t and d:
            return t, d

    if "items" in property_details:
        if any(key in property_details["items"] for key in ["oneOf", "anyOf", "allOf"]):
            t, d = _handle_array_like_property(
                property_type, property_details["items"], defs
            )
            if t and d:
                return t, d

        ref_type, ref_details = get_property_if_ref(property_details["items"], defs)
        if ref_type or ref_details:
            return property_type, ref_details
        else:
            ref_type, ref_details = _get_property_details(
                property_details["items"].get("type"), property_details["items"], defs
            )
            return property_type, ref_details

    elif "pattern" in property_details:
        pattern = property_details["pattern"]
        res_details = f"[`{pattern}`](https://regex101.com/?regex={urllib.parse.quote_plus(pattern)})"
        return property_type, res_details
    elif "const" in property_details:
        res_details = f"`{property_details.get('const')}`"
        return "const", res_details
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

        return property_type, res_details
    elif property_details.get("type") == "string":
        _format = property_details.get("format")
        _max_length = property_details.get("maxLength")
        _min_length = property_details.get("minLength")
        if _format:
            return property_type, f"Format: `{_format}`"
        elif _max_length or _min_length:
            if _max_length and _min_length:
                return (
                    property_type,
                    f"Length: `{_min_length} <= string <= {_max_length}`",
                )
            elif _max_length:
                return property_type, f"Length: `string <= {_max_length}`"
            elif _min_length:
                return property_type, f"Length: `string >= {_min_length}`"
            else:
                return property_type, f"{property_type}"
        else:
            return property_type, f"{property_type}"
    else:
        return property_type, f"{property_type}"
