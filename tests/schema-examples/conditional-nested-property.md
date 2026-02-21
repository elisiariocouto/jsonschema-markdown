# Person with Address

A person object with nested address that has conditionals.

### Type: `object`

| Property | Type | Required | Possible values | Conditional | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ----------- | ---------- | ------- | ----------- | -------- |
| name | `string` |  | string |  |  |  | Person's name |  |
| address | `object` |  | object |  |  |  | Person's address |  |
| address.country | `string` |  | string |  |  |  | Country code |  |
| address.postal_code | `string` |  | string |  |  |  | Postal code |  |
| address.postal_code | `string` |  | [`[0-9]{5}`](https://regex101.com/?regex=%5B0-9%5D%7B5%7D) | **If** country = USA |  |  |  |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
