# NullableArrays

Arrays whose items are nullable (e.g. Pydantic list[Optional[str]]) versus arrays that are themselves nullable (Optional[list[str]]).

### Type: `object`

| Property | Type | Required | Possible values | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | -------- |
| values | `array` | ✅ | string or null |  |  | list[Optional[str]]: items may be null, the array may not. |  |
| values_oneof | `array` |  | string or null |  |  | Nullable items using oneOf. |  |
| values_list_type | `array` |  | string or null |  |  | Nullable items using a list-form type. |  |
| tags | `array` |  | [Tag](#tag) or null |  |  | list[Optional[Tag]]: items are a reference or null. |  |
| optional_values | `array` or `null` |  | string |  | `null` | Optional[list[str]]: the array may be null, the items may not. |  |
| optional_values_nullable_items | `array` or `null` |  | string or null |  | `null` | Optional[list[Optional[str]]]: both the array and its items may be null. |  |
| optional_values_list_type | `array` or `null` |  | string or null |  |  | Nullable array (list-form type) with nullable items; null must appear once in the type. |  |
| nested_nullable_lists | `array` |  | array of string, or null |  |  | list[Optional[list[str]]]: the inner lists may be null, their strings may not. |  |
| nested_nullable_items | `array` |  | array of string or null |  |  | list[list[Optional[str]]]: the strings may be null, the inner lists may not. |  |
| nested_nullable_lists_list_type | `array` |  | array of string, or null |  |  | Nullable inner lists using a list-form type. |  |
| nested_mixed_items | `array` |  | integer and/or array of string, or null |  |  | Items are an integer, a list of strings or null. |  |
| enum_items | `array` |  | `x` `y` |  |  | Nullable list-form type restricted by an enum without null: null is not allowed. |  |
| const_items | `array` |  | `x` |  |  | Nullable list-form type restricted by a const: null is not allowed. |  |
| enum_or_null_items | `array` |  | `x` `y` or null |  |  | An enum or null. |  |
| only_null_items | `array` |  | null |  |  | Items may only be null. |  |
| multi_type_nullable_items | `array` |  | string or integer or null |  |  | Items with several list-form types or null. |  |
| titled_null_items | `array` |  | string or null |  |  | A null option with extra keywords is still null. |  |
| list_type_entry_items | `array` |  | integer and/or string or null |  |  | Null inside a list-form type of an anyOf entry. |  |
| nullable_ref_list_type | `array` |  | [Tag](#tag) or null |  |  | A reference with a nullable list-form type. |  |
| constraint_and_null_items | `array` |  | object |  |  | The sibling type object rules out the null entry in the anyOf: items are objects only. |  |
| constraint_and_null_items[].name | `string` |  | string |  |  |  |  |
| untyped_nullable_items | `array` |  | string or null |  |  | No type keyword: items still make this an array. |  |
| sibling_type_rules_out_null | `array` |  | string |  |  | The sibling type string rules out the null entry: items are strings only. |  |
| required_alternatives_and_null | `array` |  | object |  |  | Constraint-only anyOf plus a null entry still gives one combined row. |  |
| required_alternatives_and_null[].a and/or required_alternatives_and_null[].b | `string` |  | string |  |  |  |  |
| all_of_null_in_one_entry | `array` |  | string |  |  | allOf needs every entry to allow null, so null is not allowed. |  |
| one_of_null_in_two_entries | `array` |  | integer or string |  |  | null matches both oneOf entries, so oneOf rejects it. |  |
| untyped_nested_nullable_lists | `array` |  | array of string, or null |  |  | Inner lists without a type keyword are still nested arrays. |  |
| three_level_nested | `array` |  | array of array |  |  | Three levels of arrays keep every level. |  |
| any_value_or_null | `array` |  | Any type |  |  | An entry that accepts anything makes the items unrestricted. |  |
| duplicate_entries | `array` |  | integer or null |  |  | Entries that differ only in nullability are listed once. |  |
| one_of_required_and_nullable_type | `array` |  | object |  |  | null matches both required-only oneOf entries, so oneOf rejects it: items are objects only. |  |
| one_of_required_and_nullable_type[].a or one_of_required_and_nullable_type[].b | `string` |  | string |  |  |  |  |
| only_titled_null_entry | `array` |  | object |  |  | A combinator holding only a null entry does not merge the item rows. |  |
| only_titled_null_entry[].a | `string` | ✅ | string |  |  |  |  |
| only_titled_null_entry[].b | `integer` |  | integer |  |  |  |  |
| undescribable_or_null | `array` |  |  |  |  | Options that cannot be described claim nothing, rather than only null. |  |
| format_alternatives_nullable_type | `array` |  | string or null |  |  | format applies only to strings, so the anyOf does not rule out null. |  |


---

# Definitions

## Tag

No description provided for this model.

#### Type: `object`

| Property | Type | Required | Possible values | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | -------- |
| name | `string` | ✅ | string |  |  |  |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
