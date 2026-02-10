# Subscription with Conditional Required Fields

A subscription that requires additional fields for premium tier.

### Type: `object`

| Property | Type | Required | Possible values | Conditional | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ----------- | ---------- | ------- | ----------- | -------- |
| tier | `string` |  | `basic` `premium` |  |  |  | Subscription tier |  |
| payment_method | `string` |  | string |  |  |  | Payment method |  |
| payment_method | `string` | ✅ | string | **If** tier = premium |  |  |  |  |
| billing_address | `string` |  | string |  |  |  | Billing address |  |
| billing_address | `string` | ✅ | string | **If** tier = premium |  |  |  |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
