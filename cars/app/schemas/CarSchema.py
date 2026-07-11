from pydantic import BaseModel, Field
from enum import Enum
from app.enums import EngineType, FuelType, CarStatus


class CarCreate(BaseModel):  
    brand: str = Field(examples="Tesla")
    model: str = Field(examples="Model 3")
    year: int = Field(description="year produced")
    color: str
    vin: int
    mileage: int
    engine: EngineType
    fuel: FuelType
   
class Car(CarCreate):  
    id: int
    owner_id: int
    plate: str

class Rental(BaseModel):
    status: CarStatus
    price: int 


    