from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from cars.app.database import Base
from cars.app.enums import RentalStatus
from cars.app.models.Car import Car
from cars.app.models.User import User


class Rental(Base):
    __tablename__ = "rentals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)
    renter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[RentalStatus] = mapped_column(Enum(RentalStatus), nullable=False)

    car = relationship("Car", back_populates="rentals")
    renter = relationship("User", back_populates="rentals")
