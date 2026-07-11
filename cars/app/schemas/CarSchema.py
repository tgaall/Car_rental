from pydantic import BaseModel, Field
from cars.app.enums import EngineType, FuelType, CarStatus


class CarCreate(BaseModel):
    brand: str = Field(examples=["Tesla"])
    model: str = Field(examples=["Model 3"])
    year: int = Field(description="year produced")
    color: str
    vin: str
    mileage: int
    engine_type: EngineType
    fuel_type: FuelType


class Car(CarCreate):
    id: int
    owner_id: int
    plate: str
