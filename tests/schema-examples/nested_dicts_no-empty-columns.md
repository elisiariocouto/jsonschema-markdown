# jsonschema-markdown

JSON Schema missing a description, provide it using the `description` key in the root of the JSON document.

### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| Foobar | `object` | ✅ | object |  |
| Foobar.A | `string` |  | string |  |
| Foobar.B | `string` |  | string |  |
| Foobaz | `array` | ✅ | object |  |
| Foobaz[].C | `string` | ✅ | string |  |
| Foobaz[].D | `string` | ✅ | string |  |
| Foobaz[].E | `object` | ✅ | object |  |
| Foobaz[].E.F | `string` | ✅ | string |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
