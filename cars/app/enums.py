from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    SELLER = "Seller"
    RENTER = "Renter"


class EngineType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"


class FuelType(str, Enum):
    UNLEADED = "Unleaded"
    PREMIUM = "Premium"
    DIESEL = "Diesel"


class CarStatus(str, Enum):
    AVAILABLE = "Available"
    RENTED = "Rented"
    MAINTENANCE = "Maintenance"
    UNAVAILABLE = "Unavailable"


class RentalStatus(str, Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
