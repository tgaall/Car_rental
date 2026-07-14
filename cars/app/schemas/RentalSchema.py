from pydantic import BaseModel
from datetime import datetime
from cars.app.enums import RentalStatus


class Rental(BaseModel):
    id: int
    car_id: int
    renter_id: int
    start_date: datetime
    end_date: datetime
    total_price: int
    status: RentalStatus

    class Config:
        from_attributes = True


class CreateRent(BaseModel):
    car_id: int
    start_date: datetime
    end_date: datetime
