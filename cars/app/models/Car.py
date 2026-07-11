from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base
from app.enums import EngineType, FuelType, CarStatus

class Car(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(primary_key=True)
    plate: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)                            #→ String, Required (Tesla, BMW, etc)
    model: Mapped[str] = mapped_column(String, nullable=False)                            #→ String, Required (Model 3, 3 Series, etc)
    year: Mapped[int] = mapped_column(Integer, nullable=False)                            #→ Integer, Required (2020, 2023, etc)
    color: Mapped[str] = mapped_column(String, nullable=True)                             #→ String, Optional
    vin: Mapped[str] = mapped_column(String, unique=True)                                 #→ String, Optional, Unique
    mileage: Mapped[int] = mapped_column(Integer, nullable=True)                          #→ Integer, Optional (default: 0)
    engine_type: Mapped[EngineType] = mapped_column(Enum(EngineType))                     #→ Enum (PETROL, DIESEL, HYBRID, ELECTRIC), Required
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType))                           #→ Enum (UNLEADED, PREMIUM, DIESEL), Required
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus))                            #→ Enum (AVAILABLE, RENTED, MAINTENANCE, UNAVAILABLE), Required
    daily_rate: Mapped[int] = mapped_column(Integer, nullable=False)                      #→ Integer, Required (price per day)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)          #→ DateTime, Auto-set to now



