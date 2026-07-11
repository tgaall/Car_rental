from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from cars.app.database import Base
from cars.app.enums import EngineType, FuelType, CarStatus


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    brand: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=True)
    vin: Mapped[str] = mapped_column(String, unique=True)
    mileage: Mapped[int] = mapped_column(Integer, default=0)
    engine_type: Mapped[EngineType] = mapped_column(Enum(EngineType), nullable=False)
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType), nullable=False)
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus), nullable=False)
    daily_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    owner = relationship("User", back_populates="cars")
    rentals = relationship("Rental", back_populates="car")
