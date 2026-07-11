from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, update
from cars.app.models.Car import Car as CarModel
from cars.app.schemas.CarSchema import Car as CarSchema, CarCreate
from sqlalchemy.ext.asyncio import AsyncSession
from cars.app.dependencies import get_async_session


router = APIRouter(
    prefix="/cars",
    tags=["Cars"])

@router.get("/", response_model=list[CarSchema], status_code=200)
async def get_all_cars(session: AsyncSession = Depends(get_async_session)):
    cars = await session.scalars(
                                 select(CarModel)
                                 .where(CarModel.is_active == True)
                                 ) 
    return cars.all()

@router.get("/{car_id}", response_model=CarSchema, status_code=200)
async def get_car(car_id: int, session: AsyncSession = Depends(get_async_session)):
    car = await session.scalar(
        select(CarModel)
        .where(CarModel.id == car_id,
               CarModel.is_active == True)
    )
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return car

@router.post("/", response_model=CarSchema, status_code=201)
async def post_car(car: CarCreate, session: AsyncSession = Depends(get_async_session)):
    session_car = CarModel(**car.model_dump())
    session.add(session_car)
    await session.commit()
    return session_car  

@router.put("/{car_id}", response_model = CarSchema, status_code=200)
async def update_car(car_id: int, car_data: CarCreate, session: AsyncSession = Depends(get_async_session)):
    car = await session.scalar(
        select(CarModel).where(CarModel.id == car_id)
    )
    if not car: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await session.execute(
        update(CarModel).where(CarModel.id == car_id).values(**car_data.model_dump())
    )
    await session.commit()
    await session.refresh(car)
    return car

@router.delete("/{car_id}", response_model=CarSchema, status_code=200)
async def delete_car(car_id: int, session: AsyncSession = Depends(get_async_session)):
    car = await session.scalar(
        select(CarModel)
        .where(CarModel.id == car_id)
    )
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    await session.execute(
        update(CarModel).where(CarModel.id == car_id).values(is_active=False)
    )
    await session.commit()
    await session.refresh(car)  
    return car