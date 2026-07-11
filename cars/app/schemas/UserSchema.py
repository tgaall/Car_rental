from pydantic import BaseModel
from enum import Enum
from cars.app.enums import UserRole


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: UserRole


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    role: UserRole
