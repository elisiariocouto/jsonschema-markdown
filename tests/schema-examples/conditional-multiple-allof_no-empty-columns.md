# Multi-Country Address

Address with postal code validation for multiple countries.

### Type: `object`

| Property | Type | Required | Possible values | Conditional | Description |
| -------- | ---- | -------- | --------------- | ----------- | ----------- |
| country | `string` |  | `USA` `Canada` `UK` |  | Country code |
| postal_code | `string` |  | string |  | Postal code |
| postal_code | `string` |  | [`[0-9]{5}`](https://regex101.com/?regex=%5B0-9%5D%7B5%7D) | **If** country = USA |  |
| postal_code | `string` |  | [`[A-Z][0-9][A-Z] [0-9][A-Z][0-9]`](https://regex101.com/?regex=%5BA-Z%5D%5B0-9%5D%5BA-Z%5D+%5B0-9%5D%5BA-Z%5D%5B0-9%5D) | **If** country = Canada |  |
| postal_code | `string` |  | [`[A-Z]{1,2}[0-9]{1,2} [0-9][A-Z]{2}`](https://regex101.com/?regex=%5BA-Z%5D%7B1%2C2%7D%5B0-9%5D%7B1%2C2%7D+%5B0-9%5D%5BA-Z%5D%7B2%7D) | **If** country = UK |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
