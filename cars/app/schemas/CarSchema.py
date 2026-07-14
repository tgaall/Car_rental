from pydantic import BaseModel, Field
from cars.app.enums import EngineType, FuelType
from cars.app.enums import CarStatus


class CarCreate(BaseModel):
    brand: str
    model: str
    year: int = Field(gt=1900, description="year produced")
    color: str
    vin: str
    mileage: int = Field(gt=0)
    engine_type: EngineType
    fuel_type: FuelType
    plate: str
    daily_rate: int = Field(gt=0)


class Car(CarCreate):
    id: int
    owner_id: int
    status: CarStatus
