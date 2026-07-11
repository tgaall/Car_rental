from pydantic import BaseModel
from enum import Enum


class UserRole(str,Enum):
    ADMIN = "admin"
    SELLER = "seller"
    RENTER = "renter" 


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    role: UserRole