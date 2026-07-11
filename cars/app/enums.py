from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    RENTER = "renter"

class EngineType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    HYBRID = "hybrid"
    ELECTRIC = "electric"

class FuelType(str, Enum):
    UNLEADED = "unleaded"
    PREMIUM = "premium"
    DIESEL = "diesel"

class CarStatus(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"

class RentalStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"