# Address with Conditional Postal Code

An address object with conditional postal code format based on country.

### Type: `object`

| Property | Type | Required | Possible values | Conditional | Description |
| -------- | ---- | -------- | --------------- | ----------- | ----------- |
| country | `string` |  | string |  | Country code |
| postal_code | `string` |  | string |  | Postal code |
| postal_code | `string` |  | [`[0-9]{5}`](https://regex101.com/?regex=%5B0-9%5D%7B5%7D) | **If** country = USA |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
