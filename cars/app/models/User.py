from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Foreign_key 
from datetime import datetime
from app.database import Base
from enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique = True, nullable = False)
    phone: Mapped[str]  = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
