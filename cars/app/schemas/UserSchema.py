from pydantic import BaseModel, Field, EmailStr
from enum import Enum  # noqa: F401


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    role: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль (минимум 8 символов)")
    phone: str | None = None
    role: str = Field(
        default="Renter", pattern="^(Renter|Seller|Admin)$", description="Role"
    )
