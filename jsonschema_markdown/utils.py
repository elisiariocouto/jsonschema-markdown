def create_enum_markdown(schema: dict) -> str:
    """
    Create markdown for enum values.
    """

    markdown = "**Possible Values:** "
    markdown += " or ".join([f"`{value}`" for value in schema["enum"]]) + "\n\n"

    return markdown


def create_const_markdown(schema: dict) -> str:
    """
    Create markdown for const values.
    """

    return f"**Possible Values:** {schema.get('const', '?')}\n\n"


def sort_properties(schema: dict) -> dict:
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
