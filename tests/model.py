from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field


class ExtraPackBasic(BaseModel):
    """
    This is the description of the ExtraPack1.
    """

    heated_seats: bool = Field(
        default=False, description="Whether the car has heated seats."
    )
    heated_steering_wheel: bool = Field(
        default=False, description="Whether the car has a heated steering wheel."
    )
    parking_sensors: bool = Field(
        default=True, description="Whether the car has parking sensors."
    )


class ExtraPackAdvanced(BaseModel):
    """
    This is the description of the ExtraPack2.
    """

    heated_seats: bool = Field(
        default=True, description="Whether the car has heated seats."
    )
    heated_steering_wheel: bool = Field(
        default=True, description="Whether the car has a heated steering wheel."
    )
    parking_sensors: bool = Field(
        default=True, description="Whether the car has parking sensors."
    )
    adaptive_cruise_control: bool = Field(
        default=True, description="Whether the car has adaptive cruise control"
    )


class CarClass(BaseModel):
    """
    This is the description of the CarClass.
    """

    type: Literal["sedan", "hatchback", "suv"] = Field(
        ..., description="The type of car."
    )
    doors: int = Field(default=5, description="The number of doors the car has.")
    passengers: int = Field(
        default=5, description="The number of passengers the car can carry."
    )

    model_config = ConfigDict(title="Class")


class Engine(BaseModel):
    """
    This is the description of the Engine.

    **Markdown works**. *Italic*. **Bold**. ***Bold and italic***.
    - [] Unchecked
    - [x] Checked
    """

    model: str = Field(
        ...,
        description="The name of the engine model.",
        max_length=100,
        min_length=1,
    )
    power: int = Field(..., description="The power of the engine in HP.")
    fuel_type: Literal["gasoline", "diesel", "electric"] = Field(
        ..., description="The type of fuel the engine uses."
    )
    turbo: bool = Field(
        default=False,
        description="Whether the engine has a turbo or not.",
    )
    liters: float = Field(
        description="The displacement of the engine in liters.",
        gt=0.0,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "model": "1.6 TDI",
                    "power": 105,
                    "fuel_type": "diesel",
                    "turbo": True,
                    "liters": 1.6,
                },
                {
                    "model": "1.4 TSI",
                    "power": 150,
                    "fuel_type": "gasoline",
                    "turbo": True,
                    "liters": 1.4,
                },
                {
                    "model": "e-208",
                    "power": 136,
                    "fuel_type": "electric",
                    "turbo": False,
                    "liters": 0,
                },
            ]
        }
    )


class Airbag(BaseModel):
    """
    This is the description of the Airbag.
    """

    type: Literal["front", "side", "curtain"] = Field(
        ..., description="The type of airbag."
    )


class NavigationSystem(BaseModel):
    """
    This is the description of the NavigationSystem.
    """

    type: Literal["gps", "carplay", "androidauto"] = Field(
        ..., description="The type of navigation system."
    )


class Upholstery(BaseModel):
    """
    This is the description of the Upholstery.
    """

    type: Literal["leather", "fabric"] = Field(
        ..., description="The type of upholstery."
    )
    stitching: dict[str, str] = Field({}, description="Metadata about the stitching.")


class Car(BaseModel):
    """
    This is the description of the Car.

    New lines work.
    UTF-8 characters work: áéíóú
    👍
    """

    brand: str = Field(
        ...,
        description="The brand of the car.",
        max_length=100,
        min_length=1,
        examples=["Ford", "Toyota"],
    )
    brand_country: str = Field(
        description="[Deprecated] The country where the brand is from.",
        pattern="^[A-Z]{2}$",
    )
    model: str = Field(
        ...,
        description="The model of the car.",
        max_length=100,
        min_length=1,
        examples=["Focus", "Corolla"],
    )
    year: int = Field(
        ...,
        description="The year of the car.",
        gt=1900,
        lt=2100,
    )
    car_class: CarClass = Field(
        ...,
        description="The class of the car.",
        examples=[
            {
                "type": "sedan",
                "doors": 5,
                "passengers": 5,
            },
            {
                "type": "hatchback",
                "doors": 3,
                "passengers": 2,
            },
            {
                "type": "suv",
                "doors": 5,
                "passengers": 5,
            },
        ],
    )
    engine: Engine = Field(
        ...,
        description="The engine of the car.",
    )
    kms: int = Field(None, description="The number of kilometers the car has.")
    color: str = Field(
        ...,
        description="The color of the car.",
        max_length=100,
        min_length=1,
    )
    manufacturer_config: list[Union[Airbag, NavigationSystem, Upholstery]] = Field(
        default=[], description="The manufacturer's extras."
    )
    extra_pack: Union[ExtraPackBasic, ExtraPackAdvanced, None] = Field(
        default=None, description="The extra pack of the car."
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "brand": "Ford",
                    "brand_country": "US",
                    "model": "Focus",
                    "year": 2021,
                    "car_class": {
                        "type": "sedan",
                        "doors": 5,
                        "passengers": 5,
                    },
                    "engine": {
                        "model": "1.6 TDI",
                        "power": 105,
                        "fuel_type": "diesel",
                        "turbo": True,
                        "liters": 1.6,
                    },
                    "kms": 0,
                    "color": "black",
                }
            ]
        }
    )


if __name__ == "__main__":
    import json

    print(json.dumps(Car.model_json_schema()))
