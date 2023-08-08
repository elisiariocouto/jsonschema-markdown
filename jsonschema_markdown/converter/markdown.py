import json

from loguru import logger


def generate(schema: dict) -> str:
    markdown = ""

    # Add the title and description of the schema
    markdown += (
        f"# {schema['title']}\n\n" if "title" in schema else "jsonschema-markdown\n\n"
    )
    markdown += (
        f"{schema['description']}\n\n"
        if "description" in schema
        else "JSON Schema missing a description, provide it using the `description` key in the root of the JSON document.\n\n"
    )
    markdown += _create_table_of_properties(schema)

    markdown += "\n\n---\n\n# Definitions\n\n"

    for definition in schema.get("definitions", schema.get("$defs", {})).values():
        markdown += f"\n\n## {definition.get('title', 'No Title')}\n\n"
        markdown += f"{definition.get('description', '').strip()}\n\n"
        markdown += _create_table_of_properties(definition)

    return markdown


def _sort_properties(schema: dict) -> dict:
    """
    Sort the properties in the schema by required, making the deprecated properties last.
    """
    properties = schema["properties"]

    # Sort the properties by required
    properties = dict(
        sorted(
            properties.items(),
            key=lambda item: item[0] not in schema.get("required", []),
        )
    )

    # Sort the properties by deprecated
    properties = dict(
        sorted(
            properties.items(),
            key=lambda item: "[deprecated]"
            in str(item[1].get("description", "")).lower()
            or item[1].get("deprecated", False),
        )
    )

    return properties


def _remove_nulls(property_type: str, property_details: dict) -> tuple:
    """
    Get the possible values for a property.
    """

    if "oneOf" in property_details:
        try:
            property_details["oneOf"].remove({"type": "null"})
        except Exception:
            logger.warning("No null type in oneOf")

        if len(property_details["oneOf"]) == 1:
            return _remove_nulls("object", property_details["oneOf"][0])

    if "anyOf" in property_details:
        try:
            property_details["anyOf"].remove({"type": "null"})
        except Exception:
            logger.warning("No null type in anyOf")

        if len(property_details["anyOf"]) == 1:
            return _remove_nulls("object", property_details["anyOf"][0])

    if "allOf" in property_details:
        try:
            property_details["allOf"].remove({"type": "null"})
        except Exception:
            logger.warning("No null type in allOf")

        if len(property_details["allOf"]) == 1:
            return _remove_nulls("object", property_details["allOf"][0])

    is_const = "const" in property_details
    res_type = "const" if is_const else property_type

    if "enum" in property_details:
        res_details = ", ".join(
            [f"`{str(value)}`" for value in property_details["enum"]]
        )
    elif "oneOf" in property_details:
        res_details = ", ".join(
            [
                f"`{value.get('const') if 'const' in value else str(value)}`"
                for value in property_details["oneOf"]
            ]
        )
        if any("const" in value for value in property_details["oneOf"]):
            res_type = "const"

    elif "anyOf" in property_details:
        res_details = " or ".join(
            [
                f"`{value.get('const') if 'const' in value else str(value)}`"
                for value in property_details["anyOf"]
            ]
        )
        if any("const" in value for value in property_details["anyOf"]):
            res_type = "const"
    elif "allOf" in property_details:
        res_details = " and ".join(
            [
                f"`{value.get('const') if 'const' in value else str(value)}`"
                for value in property_details["allOf"]
            ]
        )
        if any("const" in value for value in property_details["allOf"]):
            res_type = "const"
    elif "items" in property_details:
        title = property_details["items"].get("title")
        _type = property_details["items"].get("type")
        if title:
            res_details = f"[{title}](#{title})"
        elif _type:
            res_details = f"`{_type}`"
        else:
            res_details = "yo124"
    elif "pattern" in property_details:
        pattern = property_details.get("pattern")
        res_details = pattern
    elif "additionalProperties" in property_details:
        title = property_details["additionalProperties"].get("title")
        _type = property_details["additionalProperties"].get("type")
        if title:
            res_details = f"[{title}](#{title})"
        elif _type:
            res_details = f"`{_type}`"
        else:
            res_details = "?"
    elif is_const:
        res_details = property_details.get("const")
    else:
        title = property_details.get("title")
        res_type = res_type if res_type else property_details.get("type", "??")
        if title and res_type != "string" and res_type != "boolean" and not is_const:
            res_details = f"[{title}](#{title.replace(' ', '-')})"
        elif res_type:
            res_details = f"`{res_type}`"
        else:
            res_details = "???"

    return res_type, res_details


def _create_table_of_properties(schema: dict) -> str:
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
    schema["properties"] = _sort_properties(schema)

    markdown = ""

    # Add a warning before the table to indicate if additional properties are allowed
    if not schema.get("additionalProperties", True):
        markdown += "> ⚠️ Additional properties are not allowed.\n\n"

    markdown += "| Property | Type | Required | Possible Values | Deprecated | Default | Description |\n"
    markdown += "| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |\n"

    for property_name, property_details in schema["properties"].items():
        property_type = property_details.get("type", property_details.get("const"))

        property_type, possible_values = _remove_nulls(property_type, property_details)

        default = property_details.get("default")

        markdown += (
            f"| {property_name} | {property_type.capitalize()} | "
            f"{'✅' if property_name in schema.get('required', []) else ''} | "
            f"{possible_values}| "
            f"{'⛔️' if '[deprecated]' in str(property_details.get('description','')).lower() or property_details.get('deprecated') else ''} | "
            f"{'`'+json.dumps(default)+'`' if default else ''} | "
            f"{property_details.get('description','')} |\n"
        )

    return markdown
