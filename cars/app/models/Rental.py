from sqlalchemy import Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from cars.app.database import Base
from cars.app.enums import RentalStatus


class Rental(Base):
    __tablename__ = "rentals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)
    renter_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[RentalStatus] = mapped_column(
        Enum(RentalStatus), default=RentalStatus.PENDING, nullable=False
    )

    car = relationship("Car", back_populates="rentals")
    renter = relationship("User", back_populates="rentals")
