import json


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

    for definition in schema.get("definitions", {}).values():
        markdown += f"\n\n## {definition.get('title', 'No Title')}\n\n"
        markdown += f"{definition.get('description', '')}\n\n"
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
        property_type = property_details.get("type", "?")

        if "enum" in property_details:
            possible_values = ", ".join(
                [f"`{str(value)}`" for value in property_details["enum"]]
            )
        elif "oneOf" in property_details:
            possible_values = ", ".join(
                [f"`{str(value)}`" for value in property_details["oneOf"]]
            )
            property_type = "array (`oneOf`)"
        elif "anyOf" in property_details:
            possible_values = " or ".join(
                [f"`{str(value)}`" for value in property_details["anyOf"]]
            )
            property_type = "array (`anyOf`)"
        elif "allOf" in property_details:
            possible_values = " and ".join(
                [
                    f"[{value.get('title')}]({value.get('title')})"
                    for value in property_details["allOf"]
                ]
            )
            property_type = "array (`allOf`)"
        elif "items" in property_details:
            title = property_details["items"].get("title")
            _type = property_details["items"].get("type")
            if title:
                possible_values = f"[{title}](#{title})"
            elif _type:
                possible_values = f"`{_type}`"
            else:
                possible_values = "??"
        elif "pattern" in property_details:
            pattern = property_details.get("pattern")
            possible_values = pattern
        elif "additionalProperties" in property_details:
            title = property_details["additionalProperties"].get("title")
            _type = property_details["additionalProperties"].get("type")
            if title:
                possible_values = f"[{title}](#{title})"
            elif _type:
                possible_values = f"`{_type}`"
            else:
                possible_values = "???"
        else:
            possible_values = f"`{property_type}`"

        markdown += (
            f"| {property_name} | {property_type.capitalize()} | "
            f"{'✅' if property_name in schema.get('required', []) else ''} | "
            f"{possible_values}| "
            f"{'⛔️' if '[deprecated]' in str(property_details.get('description','')).lower() or property_details.get('deprecated') else ''} | "
            f"{json.dumps(property_details.get('default')) if 'default' in property_details else ''} | "
            f"{property_details.get('description','')} |\n"
        )

    return markdown
