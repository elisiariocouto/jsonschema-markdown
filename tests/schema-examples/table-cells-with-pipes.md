# PipesInTableCells

Pipe characters in any table cell must be escaped so they do not split the row.

### Type: `object`

| Property | Type | Required | Possible values | Deprecated | Default | Description | Examples |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- | -------- |
| description_pipe | `string` | ✅ | string |  |  | A Python type hint such as list[str \| None]. |  |
| pre_escaped_description | `string` |  | string |  |  | Already escaped: a \| b stays as written. |  |
| default_pipe | `string` |  | string |  | `"a\|b"` | Default value containing a pipe. |  |
| examples_pipe | `string` |  | string |  |  | Example containing a pipe. | ```x\|y``` |
| enum_pipe | `string` |  | `a\|b` `c` |  |  | Enum value containing a pipe. |  |
| const_pipe | `const` |  | `a\|b` |  |  | Const value containing a pipe. |  |
| pattern_pipe | `string` |  | [`^(a\|b)$`](https://regex101.com/?regex=%5E%28a%7Cb%29%24) |  |  | Pattern alternation, escaped once. |  |
| name\|with\|pipes | `string` |  | string |  |  | Property name containing pipes. |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
