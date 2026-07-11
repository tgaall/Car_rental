from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Foreign_key 
from datetime import datetime
from app.database import Base
from app.enums import RentalStatus
from app.models.Car import Car
from app.models.User import User

class Rental(Base):
    __tablename__ = 'rentals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(Integer, Foreign_key('cars.id'), nullable=False)
    renter_id: Mapped[int] = mapped_column(Integer, Foreign_key("users.id"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[RentalStatus] = mapped_column(Enum(RentalStatus))
    