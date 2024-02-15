# Car

This is the description of the Car.

New lines work.
UTF-8 characters work: áéíóú
👍

| Property | Type | Required | Possible Values | Deprecated | Default | Description |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |
| brand | `string` | ✅ | string|  |  | The brand of the car. |
| model | `string` | ✅ | string|  |  | The model of the car. |
| year | `integer` | ✅ | `1900 < x < 2100`|  |  | The year of the car. |
| car_class | `object` | ✅ | [CarClass](#carclass)|  |  | The class of the car. |
| engine | `object` | ✅ | [Engine](#engine)|  |  | The engine of the car. |
| color | `string` | ✅ | string|  |  | The color of the car. |
| kms | `integer` |  | integer|  |  | The number of kilometers the car has. |
| manufacterer_config | `object` |  | [Airbag](#airbag) and/or [NavigationSystem](#navigationsystem) and/or [Upholstery](#upholstery)|  |  | The manufacturer's extras. |
| brand_country | `string` | ✅ | [`^[A-Z]{2}$`](https://regex101.com/?regex=%5E%5BA-Z%5D%7B2%7D%24)| ⛔️ |  | [Deprecated] The country where the brand is from. |


---

# Definitions



## Airbag

This is the description of the AirbagExtra.

**Type:** `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |
| type | `string` | ✅ | `front` `side` `curtain`|  |  | The type of airbag. |


## Class

This is the description of the CarClass.

**Type:** `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |
| type | `string` | ✅ | `sedan` `hatchback` `suv`|  |  | The type of car. |
| doors | `integer` |  | integer|  | `5` | The number of doors the car has. |
| passengers | `integer` |  | integer|  | `5` | The number of passengers the car can carry. |


## Engine

This is the description of the Engine.

**Markdown works**. *Italic*. **Bold**. ***Bold and italic***.
- [] Unchecked
- [x] Checked

**Type:** `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |
| model | `string` | ✅ | string|  |  | The name of the engine model. |
| power | `integer` | ✅ | integer|  |  | The power of the engine in HP. |
| fuel_type | `string` | ✅ | `gasoline` `diesel` `electric`|  |  | The type of fuel the engine uses. |
| liters | `number` | ✅ | `0.0 < x `|  |  | The displacement of the engine in liters. |
| turbo | `boolean` |  | boolean|  |  | Whether the engine has a turbo or not. |


## NavigationSystem

This is the description of the NavigationSystem.

**Type:** `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |
| type | `string` | ✅ | `gps` `carplay` `androidauto`|  |  | The type of navigation system. |


## Upholstery

This is the description of the Upholstery.

**Type:** `object`

| Property | Type | Required | Possible Values | Deprecated | Default | Description |
| -------- | ---- | -------- | --------------- | ---------- | ------- | ----------- |
| type | `string` | ✅ | `leather` `fabric`|  |  | The type of upholstery. |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
