# NullableObjectNested

Schema with a nullable object property that still has nested fields rendered.

### Type: `object`

| Property | Type | Required | Possible values | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | -------- |
| profile | `object` or `null` | ✅ | object |  |  | User profile, or null if anonymous. |  |
| profile.first_name | `string` | ✅ | string |  |  |  |  |
| profile.last_name | `string` |  | string |  |  |  |  |
| history | `array` or `null` |  | object |  |  | Action history or null. |  |
| history[].action | `string` |  | string |  |  |  |  |
| history[].timestamp | `string` |  | Format: [`date-time`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats) |  |  |  |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
