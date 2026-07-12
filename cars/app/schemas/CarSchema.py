from pydantic import BaseModel, Field
from cars.app.enums import EngineType, FuelType


class CarCreate(BaseModel):
    brand: str
    model: str
    year: int = Field(description="year produced")
    color: str
    vin: str
    mileage: int
    engine_type: EngineType
    fuel_type: FuelType
    plate: str
    daily_rate: int


class Car(CarCreate):
    id: int
    owner_id: int
    plate: str
