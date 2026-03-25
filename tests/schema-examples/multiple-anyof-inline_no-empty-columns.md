# StudioAudit

JSON Schema missing a description, provide it using the `description` key in the root of the JSON document.

### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| scene_time | `string` | ✅ | Format: [`date-time`](https://json-schema.org/understanding-json-schema/reference/string#built-in-formats) |  |
| cinema_event | `object` | ✅ | [BoxOfficeAction](#boxofficeaction) and/or [CastingSlotAction](#castingslotaction) and/or [CrewEvent](#crewevent) and/or [DirectorVerdict](#directorverdict) and/or [PremiereEvent](#premiereevent) and/or [PropVaultAction](#propvaultaction) and/or [SetRenaming](#setrenaming) |  |


---

# Definitions

## DirectorVerdict

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| studio_lot | `string` | ✅ | string |  |  |
| director_contact | `string` | ✅ | string |  |  |
| producer_contact | `string` | ✅ | string |  |  |
| franchise | `string` | ✅ | string |  |  |
| release_stage | `string` | ✅ | string |  |  |
| verdict | `string` | ✅ | string |  |  |
| reel_code | `string` | ✅ | string |  |  |
| screening_id | `string` | ✅ | string |  |  |
| kind | `const` |  | `director_verdict` | `"director_verdict"` |  |
| character_arc | `string` or `null` |  | string | `null` |  |
| cut_style | `string` or `null` |  | string | `null` |  |

## PropVaultAction

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| crew_member | `string` | ✅ | string |  |  |
| prop_name | `string` | ✅ | string |  |  |
| studio_lot | `string` | ✅ | string |  |  |
| franchise | `string` | ✅ | string |  |  |
| release_stage | `string` | ✅ | string |  |  |
| action | `string` | ✅ | string |  |  |
| kind | `const` |  | `prop_vault_action` | `"prop_vault_action"` |  |

## Credit

No description provided for this model.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| contact | `string` | ✅ | string |  |  |
| stage_name | `string` | ✅ | string |  |  |
| mark_ms | `integer` | ✅ | integer |  |  |
| commentary | `string` or `null` |  | string | `null` |  |

## CastingSlotAction

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| phase_state | `string` | ✅ | string |  |  |
| kind | `const` |  | `casting_slot_action` | `"casting_slot_action"` |  |
| final_notes | `object` or `null` |  | [Credit](#credit) | `null` |  |
| character_arc | `string` or `null` |  | string | `null` |  |
| production_meta | `object` or `null` |  | object | `null` |  |
| audition_notes | `object` or `null` |  | [Credit](#credit) | `null` |  |
| casting_lane | `string` or `null` |  | `ensemble` `lead` `franchise` | `null` |  |

## SetRenaming

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| old_set | `string` | ✅ | string |  |  |
| new_set | `string` | ✅ | string |  |  |
| release_stage | `string` | ✅ | string |  |  |
| franchise | `string` | ✅ | string |  |  |
| reel_code | `string` | ✅ | string |  |  |
| studio_project_id | `string` | ✅ | string |  |  |
| screening_id | `string` | ✅ | string |  |  |
| kind | `const` |  | `set_renaming` | `"set_renaming"` |  |

## BoxOfficeAction

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| analyst | `string` | ✅ | string |  |  |
| franchise | `string` | ✅ | string |  |  |
| updated_gross | `number` | ✅ | number |  |  |
| action | `string` | ✅ | string |  |  |
| market | `string` | ✅ | string |  |  |
| kind | `const` |  | `box_office_action` | `"box_office_action"` |  |
| prior_gross | `number` or `null` |  | number | `null` |  |

## PremiereEvent

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| event_kind | `string` | ✅ | `shoot_started` `shoot_paused` `shoot_resumed` `shoot_wrapped` `shoot_failed` |  |  |
| release_stage | `string` | ✅ | string |  |  |
| franchise | `string` | ✅ | string |  |  |
| reel_code | `string` | ✅ | string |  |  |
| screening_id | `string` | ✅ | string |  |  |
| festival_id | `string` | ✅ | string |  |  |
| kind | `const` |  | `premiere_event` | `"premiere_event"` |  |
| scene_hash | `string` or `null` |  | string | `null` |  |
| studio_project_id | `string` or `null` |  | string | `null` |  |

## CrewEvent

No description provided for this model.

#### Type: `object`

> ⚠️ Additional properties are not allowed.

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| event_kind | `string` | ✅ | `crew_called` `crew_wrapped` `crew_issue` |  |  |
| release_stage | `string` | ✅ | string |  |  |
| franchise | `string` | ✅ | string |  |  |
| screening_id | `string` | ✅ | string |  |  |
| crew_unit | `string` | ✅ | string |  |  |
| act | `string` | ✅ | string |  |  |
| reel_code | `string` | ✅ | string |  |  |
| outcome | `object` or `null` | ✅ | object |  |  |
| kind | `const` |  | `crew_event` | `"crew_event"` |  |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
