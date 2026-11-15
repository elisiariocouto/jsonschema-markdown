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
