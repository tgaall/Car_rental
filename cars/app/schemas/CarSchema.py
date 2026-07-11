from pydantic import BaseModel, Field
from enum import Enum



class Car(BaseModel):
    id: int
    owner_id: int
    plate: str

class EngineType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    HYBRID = "hybrid"
    ELECTRIC = "electric"
    

class FuelType(str, Enum):
    UNLEADED = "unleaded"
    PREMIUM = "premium"
    DIESEL = "diesel"

class CarInfo(BaseModel):
    brand: str = Field(examples="Tesla")
    model: str = Field(examples="Model 3")
    year: int = Field(description="year produced")
    color: str
    vin: int
    mileage: int
    engine: EngineType
    fuel: FuelType

class CarStatus(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"

class Rental(BaseModel):
    status: CarStatus
    price: int 


    