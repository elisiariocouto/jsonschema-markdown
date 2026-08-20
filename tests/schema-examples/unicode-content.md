# Café Menu — Spécialités

Schema with non-ASCII content: accents, em dashes — and CJK (日本語).

### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | -------- |
| plat | `string` | ✅ | string |  | `"crème brûlée"` | Le plat du jour — crème brûlée 🍮 |  |
| prix | `number` | ✅ | `0 <= x ` |  |  | Prix en € (euros) |  |
| größe | `string` |  | `klein` `mittel` `groß` |  |  | Portionsgröße |  |
| 説明 | `string` |  | string |  |  | 日本語の説明 — CJK property name |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
