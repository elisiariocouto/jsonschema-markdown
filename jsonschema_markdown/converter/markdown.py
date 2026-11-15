import copy
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


def _type_matches(prop_type: str | list | None, target: str) -> bool:
    """True if prop_type equals target or is a list containing target (nullable form)."""
    if prop_type == target:
        return True
    return isinstance(prop_type, list) and target in prop_type


def _format_example(example, examples_format, sort_yaml_keys=False):
    """
    Format the example based on the examples_format. Only works for dict.
    """

    try:
        if examples_format == "yaml":
            if isinstance(example, dict):
                return f"```yaml\n{yaml.dump(example, sort_keys=sort_yaml_keys, allow_unicode=True).strip()}\n```"
            else:
                return f"```yaml\n{example}\n```"
        elif examples_format == "json":
            if isinstance(example, dict):
                return (
                    f"```json\n{json.dumps(example, indent=2, ensure_ascii=False)}\n```"
                )
            else:
                return f"```json\n{example}\n```"
    except Exception:  # noqa: BLE001 - fall back to a plain code block
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


def _extract_inline_defs(schema: dict) -> dict:
    """
    Walk the schema tree and extract inline object definitions from
    anyOf/oneOf/allOf combinators into $defs, replacing them with $ref.

    Returns a new schema dict (deep copy) with inline objects promoted to $defs.
    """
    schema = copy.deepcopy(schema)

    defs_key = "definitions" if "definitions" in schema else "$defs"

    if defs_key not in schema:
        schema[defs_key] = {}

    defs = schema[defs_key]
    counter = [0]

    def _make_ref(name: str) -> dict:
        return {"$ref": f"#/{defs_key}/{name}"}

    def _choose_name(obj: dict) -> str:
        title = obj.get("title")
        if not title:
            counter[0] += 1
            return f"InlineObject{counter[0]}"

        name = title
        if name in defs:
            if defs[name] == obj:
                return name
            suffix = 2
            while f"{title}_{suffix}" in defs:
                suffix += 1
            return f"{title}_{suffix}"
        return name

    def _is_extractable(entry: dict) -> bool:
        if not isinstance(entry, dict) or "$ref" in entry:
            return False
        has_properties = bool(entry.get("properties"))
        is_object = _type_matches(entry.get("type"), "object") or (
            has_properties and "type" not in entry
        )
        return is_object and has_properties

    def _process_combinator(parent: dict, combinator_key: str):
        entries = parent[combinator_key]
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            _walk(entry)
            if _is_extractable(entry):
                name = _choose_name(entry)
                if name not in defs:
                    defs[name] = entry
                entries[i] = _make_ref(name)

    def _walk(node: dict):
        if not isinstance(node, dict):
            return

        for prop_details in node.get("properties", {}).values():
            if not isinstance(prop_details, dict):
                continue

            for combinator in ("anyOf", "oneOf", "allOf"):
                if combinator in prop_details:
                    _process_combinator(prop_details, combinator)

            items = prop_details.get("items")
            if isinstance(items, dict):
                for combinator in ("anyOf", "oneOf", "allOf"):
                    if combinator in items:
                        _process_combinator(items, combinator)
                _walk(items)

            _walk(prop_details)

    _walk(schema)

    for def_name in list(defs.keys()):
        _walk(defs[def_name])

    if not defs:
        del schema[defs_key]

    return schema


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

    _schema = _extract_inline_defs(_schema)
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
            "`" + json.dumps(prop_details.get("default"), ensure_ascii=False) + "`"
            if has_default_value
            else ""
        )
        description = prop_details.get("description", "").strip(" \n")

        # Replace newlines in description with <br /> for markdown to prevent table breaking
        if "\n" in description:
            description = description.replace("\n", "<br />")

        examples = ", ".join(
            [f"```{example!s}```" for example in prop_details.get("examples", [])]
        )

        # Add the current property to our results
        item = {
            "property": full_path,
            "type": property_type,
            "required": "✅" if prop_name in required_props else "",
            "possible_values": possible_values,
            "conditional": "",
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
        if _type_matches(prop_type, "object") and prop_details.get("properties"):
            nested_items = _process_properties_recursively(
                prop_details["properties"],
                full_path,
                prop_details.get("required", []),
                defs,
                conditional_properties,
            )
            table_items.extend(nested_items)

        # If this is an array with items that are objects, process them too
        elif _type_matches(prop_type, "array") and isinstance(
            prop_details.get("items"), dict
        ):
            items_schema = prop_details["items"]
            if _type_matches(items_schema.get("type"), "object") and items_schema.get(
                "properties"
            ):
                array_path = f"{full_path}[]"  # Add [] to indicate array items
                _combinator_key = _get_combinator_key(items_schema)
                _non_null_entries = (
                    _split_null(items_schema[_combinator_key], _combinator_key)[0]
                    if _combinator_key is not None
                    else []
                )
                if _non_null_entries and all(
                    _is_constraint_only(e) for e in _non_null_entries
                ):
                    # The combinator entries are pure constraints (e.g. required only),
                    # not type alternatives; null entries say nothing about the
                    # objects' properties. Emit a single combined row for all properties.
                    combined_name = _COMBINATOR_SEPARATORS[_combinator_key].join(
                        f"{array_path}.{p}" for p in items_schema["properties"]
                    )
                    all_prop_types = []
                    all_prop_values = []
                    for _prop in items_schema["properties"].values():
                        _p_type, _p_values = _get_property_details(
                            _prop.get("type"), _prop, defs
                        )
                        all_prop_types.append(_p_type)
                        all_prop_values.append(_p_values)
                    distinct_types = {t for t in all_prop_types if t}
                    if len(distinct_types) == 1:
                        combined_type = next(iter(distinct_types))
                        combined_values = next((v for v in all_prop_values if v), "")
                    else:
                        combined_type = (
                            ", ".join(sorted(distinct_types)) if distinct_types else ""
                        )
                        combined_values = ""
                    combined_item = {
                        "property": combined_name,
                        "type": combined_type,
                        "required": "",
                        "possible_values": combined_values,
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
        if isinstance(prop_details, dict) and _type_matches(
            prop_details.get("type"), "object"
        ):
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
        "not",
        "if",
        "then",
        "else",
        "prefixItems",
        "contains",
        "patternProperties",
        "propertyNames",
        "contentEncoding",
        "contentMediaType",
        "contentSchema",
    }
)


_COMBINATOR_SEPARATORS = {"oneOf": " or ", "anyOf": " and/or ", "allOf": " and "}


# Keywords that only annotate a schema: one made of nothing else accepts any value
_ANNOTATION_KEYS = frozenset(
    {
        "title",
        "description",
        "$comment",
        "default",
        "examples",
        "deprecated",
        "readOnly",
        "writeOnly",
    }
)


def _accepts_anything(schema: dict) -> bool:
    """True if schema places no restriction on values, e.g. {} or {"description": ...}."""
    return all(key in _ANNOTATION_KEYS for key in schema)


def _is_array_schema(schema: dict) -> bool:
    """True for an array schema, including one that omits "type" but has items."""
    return schema.get("type") == "array" or ("type" not in schema and "items" in schema)


def _strip_null(schema: dict) -> tuple[dict | None, bool | None]:
    """
    Separate null from a schema's own "type" without modifying the schema.

    Returns the schema without null (None when it only allows null) and whether
    its type allows null: True or False, or None when it has no type to decide.
    Schemas with enum or const already list the exact values allowed, so they
    are returned as is and rule null out.
    """
    if "enum" in schema or "const" in schema:
        return schema, False
    schema_type = schema.get("type")
    if schema_type is None:
        return schema, None
    if schema_type == "null":
        return None, True
    if not isinstance(schema_type, list) or "null" not in schema_type:
        return schema, False
    remaining = [t for t in schema_type if t != "null"]
    if not remaining:
        return None, True
    return {**schema, "type": remaining[0] if len(remaining) == 1 else remaining}, True


def _matches_null(entry: dict) -> bool:
    """
    True if null validates against entry. Keywords such as format, required or
    properties only apply to strings or objects, so an entry without a type
    accepts null; a $ref or nested combinator is not followed and counts as not.
    """
    _, type_allows_null = _strip_null(entry)
    if type_allows_null is not None:
        return type_allows_null
    return not any(key in entry for key in ("$ref", "anyOf", "oneOf", "allOf", "not"))


def _split_null(entries: list, combinator: str) -> tuple[list, bool | None]:
    """
    Separate null from oneOf/anyOf/allOf entries without modifying them.

    Returns the entries without null and the combinator's decision on null:
    False if null fails it (anyOf needs one entry matching null, oneOf exactly
    one, allOf every entry), True if null passes and an entry offers it
    explicitly, and None if null passes without being mentioned, e.g. when
    every entry only holds "required".
    """
    non_null = []
    offers_null = False
    for entry in entries:
        stripped, type_allows_null = _strip_null(entry)
        if stripped is not None:
            non_null.append(stripped)
        offers_null = offers_null or bool(type_allows_null)

    matches = [_matches_null(entry) for entry in entries]
    if combinator == "anyOf":
        valid = any(matches)
    elif combinator == "oneOf":
        valid = matches.count(True) == 1
    else:
        valid = all(matches)
    if not valid:
        return non_null, False
    return non_null, True if offers_null else None


def _allows_null(*decisions: bool | None) -> bool:
    """
    Combine null decisions from keywords that all apply to the same value, such
    as a schema's own type and its combinator: null is allowed when one of them
    allows it and none rules it out.
    """
    decided = [d for d in decisions if d is not None]
    return bool(decided) and all(decided)


def _is_constraint_only(schema_entry: dict) -> bool:
    """Return True if entry has only constraint keywords (e.g. required), no type info."""
    return not any(key in schema_entry for key in _TYPE_INFO_KEYS)


def _get_combinator_key(schema: dict) -> str | None:
    """Return the first combinator keyword found in schema, or None."""
    for key in ("oneOf", "anyOf", "allOf"):
        if key in schema:
            return key
    return None


def _handle_array_like_property(property_type: str, property_details: dict, defs: dict):
    """
    Handle properties that combine schemas with oneOf, anyOf or allOf.
    """
    array_type = _get_combinator_key(property_details)

    if array_type is None:
        logger.warning(
            f"Array-like property without oneOf, anyOf or allOf: {property_type} {property_details}"
        )
        # TODO: Support for items, prefixItems, contains, minContains, maxContains, uniqueItems, unevaluatedItems
        # https://json-schema.org/understanding-json-schema/reference/array
        return f"`{property_type}`", {}

    entries, combinator_null = _split_null(property_details[array_type], array_type)
    allows_null = _allows_null(_strip_null(property_details)[1], combinator_null)

    types = []
    details = []

    for value in entries:
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

    non_null_details = sorted(d for d in details if d is not None)
    possible_values = _COMBINATOR_SEPARATORS[array_type].join(non_null_details)

    # Return the types of the nested oneOf, anyOf or allOf, deduplicated and
    # with null at the end if present
    if allows_null:
        types.append("`null`")
    types = sorted(set(types))
    if "`null`" in types:
        types.remove("`null`")
        types.append("`null`")
    return " or ".join(types), possible_values


def _describe_items(items: dict, defs: dict) -> str:
    """
    Describe the possible values of an array's items, e.g. "string or null".

    A null option makes the items nullable (list[str | None]), not the array
    itself, so it is described here instead of in the array's type.
    """
    schema, own_null = _strip_null(items)
    if schema is None:
        return "null"

    combinator = _get_combinator_key(schema)
    alternatives, combinator_null = [], None
    if combinator:
        entries = schema[combinator]
        # An anyOf/oneOf entry that accepts anything leaves the items unrestricted
        if combinator == "allOf" or not any(_accepts_anything(e) for e in entries):
            non_null, combinator_null = _split_null(entries, combinator)
            alternatives = [e for e in non_null if not _is_constraint_only(e)]
        schema = {k: v for k, v in schema.items() if k != combinator}
    # The schema's own type and its combinator both apply, e.g. a sibling
    # "type": "object" rules out a null entry in the anyOf
    allows_null = _allows_null(own_null, combinator_null)

    # Nested arrays go last so "integer and/or array of string" stays readable
    descriptions = sorted(
        {d for d in (_describe_element(e, defs) for e in alternatives) if d},
        key=lambda d: (d.startswith("array of "), d),
    )
    if descriptions:
        description = _COMBINATOR_SEPARATORS[combinator].join(descriptions)
    elif alternatives and _accepts_anything(schema):
        # Options exist (e.g. {"format": "date"}) but none can be described:
        # claim nothing rather than suggest the items can only be null
        return ""
    elif combinator_null is not None and _accepts_anything(schema):
        # The combinator only offered null and nothing else describes the items
        description = ""
    else:
        # No combinator, or one that only adds constraints (e.g. required) or null
        description = _describe_element(schema, defs)

    if not allows_null:
        return description
    if not description:
        return "null"
    # The comma attaches null to the items, not to a nested array's own items:
    # "array of string, or null" vs "array of string or null"
    nested_array = any(_is_array_schema(e) for e in alternatives or [schema])
    return f"{description}{', or' if nested_array else ' or'} null"


def _describe_element(schema: dict, defs: dict) -> str:
    """Describe one kind of value an array may hold; nested arrays read "array of X"."""
    ref_type, ref_details = get_property_if_ref(schema, defs)
    if ref_type or ref_details:
        return ref_details
    if _accepts_anything(schema):
        return "Any type"
    if _is_array_schema(schema):
        inner = _describe_items(schema["items"], defs) if "items" in schema else ""
        return f"array of {inner}" if inner else "array"

    schema_type = schema.get("type")
    type_names, details = _get_property_details(schema_type, schema, defs)
    if not details and schema_type is not None:
        # Several list-form types (e.g. ["string", "integer"]) are only named in the type
        details = type_names.replace("`", "")
    return details or ""


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

    # Normalize list-form types (e.g. ["object", "null"]) into a recognizable
    # base type plus an optional "or null" suffix so the rest of this function
    # can rely on scalar type strings.
    if isinstance(property_type, list):
        non_null = [t for t in property_type if t != "null"]
        has_null = "null" in property_type
        if len(non_null) == 1:
            base_type, base_details = _get_property_details(
                non_null[0], property_details, defs
            )
            if has_null:
                return f"{base_type} or `null`", base_details
            return base_type, base_details
        types = " or ".join(f"`{t}`" for t in property_type)
        return types, ""

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
            " ".join([f"`{value!s}`" for value in property_details["enum"]]),
        )

    # Handle array-like properties
    if any(key in property_details for key in ["oneOf", "anyOf", "allOf"]):
        t, d = _handle_array_like_property(property_type, property_details, defs)
        if t and d:
            return t, d

    if "items" in property_details:
        # A schema with items describes an array even when "type" is omitted
        return (
            f"`{property_type or 'array'}`",
            _describe_items(property_details["items"], defs),
        )
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
