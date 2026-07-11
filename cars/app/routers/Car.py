from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from cars.app.models.Car import Car as CarModel
from cars.app.schemas.CarSchema import Car
from cars.app.database import get_db
from sqlalchemy.orm import Session  


router = APIRouter(
    prefix="/cars"
    tags=["Cars"]
)

@router.get("/", response_model=Car, status_code=200)
async def get_all_cars(db: Session = Depends(get_db)):
    stmt = 