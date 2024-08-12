# jsonschema-markdown

JSON Schema missing a description, provide it using the `description` key in the root of the JSON document.

### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| firstName | `string` |  | string |  | The person's first name. |
| lastName | `string` |  | string |  | The person's last name. |
| age | `integer` |  | `0 <= x <= 150` and multiple of `1` | `25` | Age in years which must be equal to or greater than zero. |
| email | `string` |  | Format: [`email`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats) |  | Email address of the person. |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
