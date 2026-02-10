# User Account with Age Restrictions

User account with conditional requirements based on age.

### Type: `object`

| Property | Type | Required | Possible values | Conditional | Description |
| -------- | ---- | -------- | --------------- | ----------- | ----------- |
| age | `integer` |  | integer |  | User's age |
| parental_consent | `string` |  | string |  | Parental consent document |
| parental_consent | `string` |  | [`^consent-[a-z0-9]+$`](https://regex101.com/?regex=%5Econsent-%5Ba-z0-9%5D%2B%24) | **If** age <= 18 |  |
| email | `string` |  | string |  | Email address |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
