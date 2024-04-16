# Car

This is the description of the Car.

New lines work.
UTF-8 characters work: áéíóú
👍

### Examples

```
{'brand': 'Ford', 'brand_country': 'US', 'car_class': {'doors': 5, 'passengers': 5, 'type': 'sedan'}, 'color': 'black', 'engine': {'fuel_type': 'diesel', 'liters': 1.6, 'model': '1.6 TDI', 'power': 105, 'turbo': True}, 'kms': 0, 'model': 'Focus', 'year': 2021}
```

### Type: `object`

| Property | Type | Required | Possible values | Deprecated | Description | Examples |
| -------- | ---- | -------- | --------------- | ---------- | ----------- | -------- |
| brand | `string` | ✅ | Length: `1 <= string <= 100` |  | The brand of the car. | ```Ford```, ```Toyota``` |
| model | `string` | ✅ | Length: `1 <= string <= 100` |  | The model of the car. | ```Focus```, ```Corolla``` |
| year | `integer` | ✅ | `1900 < x < 2100` |  | The year of the car. |  |
| car_class | `object` | ✅ | [CarClass](#carclass) |  | The class of the car. | ```{'doors': 5, 'passengers': 5, 'type': 'sedan'}```, ```{'doors': 3, 'passengers': 2, 'type': 'hatchback'}```, ```{'doors': 5, 'passengers': 5, 'type': 'suv'}``` |
| engine | `object` | ✅ | [Engine](#engine) |  | The engine of the car. |  |
| color | `string` | ✅ | Length: `1 <= string <= 100` |  | The color of the car. |  |
| kms | `integer` |  | integer |  | The number of kilometers the car has. |  |
| manufacturer_config | `array` |  | [Airbag](#airbag) and/or [NavigationSystem](#navigationsystem) and/or [Upholstery](#upholstery) |  | The manufacturer's extras. |  |
| brand_country | `string` | ✅ | [`^[A-Z]{2}$`](https://regex101.com/?regex=%5E%5BA-Z%5D%7B2%7D%24) | ⛔️ | [Deprecated] The country where the brand is from. |  |


---

# Definitions

## Airbag

This is the description of the Airbag.

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| type | `string` | ✅ | `front` `side` `curtain` | The type of airbag. |
## Class

This is the description of the CarClass.

#### Type: `object`

| Property | Type | Required | Possible values | Default | Description |
| -------- | ---- | -------- | --------------- | ------- | ----------- |
| type | `string` | ✅ | `sedan` `hatchback` `suv` |  | The type of car. |
| doors | `integer` |  | integer | `5` | The number of doors the car has. |
| passengers | `integer` |  | integer | `5` | The number of passengers the car can carry. |
## Engine

This is the description of the Engine.

**Markdown works**. *Italic*. **Bold**. ***Bold and italic***.
- [] Unchecked
- [x] Checked

#### Examples

```
{'fuel_type': 'diesel', 'liters': 1.6, 'model': '1.6 TDI', 'power': 105, 'turbo': True}
```

```
{'fuel_type': 'gasoline', 'liters': 1.4, 'model': '1.4 TSI', 'power': 150, 'turbo': True}
```

```
{'fuel_type': 'electric', 'liters': 0, 'model': 'e-208', 'power': 136, 'turbo': False}
```

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| model | `string` | ✅ | Length: `1 <= string <= 100` | The name of the engine model. |
| power | `integer` | ✅ | integer | The power of the engine in HP. |
| fuel_type | `string` | ✅ | `gasoline` `diesel` `electric` | The type of fuel the engine uses. |
| liters | `number` | ✅ | `0.0 < x ` | The displacement of the engine in liters. |
| turbo | `boolean` |  | boolean | Whether the engine has a turbo or not. |
## NavigationSystem

This is the description of the NavigationSystem.

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| type | `string` | ✅ | `gps` `carplay` `androidauto` | The type of navigation system. |
## Upholstery

This is the description of the Upholstery.

#### Type: `object`

| Property | Type | Required | Possible values | Description |
| -------- | ---- | -------- | --------------- | ----------- |
| type | `string` | ✅ | `leather` `fabric` | The type of upholstery. |
| stitching | `object` |  | object | Metadata about the stitching. |


---

Markdown generated with [jsonschema-markdown](https://github.com/elisiariocouto/jsonschema-markdown).
