# Address with If/Then/Else

An address with conditional structure based on country.

### Type: `object`

| Property | Type | Required | Possible values | Conditional | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ----------- | ---------- | ------- | ----------- | -------- |
| country | `string` |  | string |  |  |  | Country code |  |
| postal_code | `string` |  | string |  |  |  | Postal code |  |
| postal_code | `string` |  | [`[0-9]{5}`](https://regex101.com/?regex=%5B0-9%5D%7B5%7D) | **If** country = USA |  |  |  |  |
| postal_code | `string` |  | [`[A-Z]{2}[0-9]{5}`](https://regex101.com/?regex=%5BA-Z%5D%7B2%7D%5B0-9%5D%7B5%7D) | **If NOT** country = USA |  |  |  |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
