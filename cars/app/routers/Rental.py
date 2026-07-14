from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from cars.app.enums import CarStatus
from cars.app.models.Rental import Rental as RentalModel
from cars.app.schemas.RentalSchema import (
    Rental as RentalSchema,
    CreateRent,
    PriceResult,
)
from cars.app.enums import RentalStatus
from cars.app.models.User import User as UserModel
from cars.app.models.Car import Car as CarModel
from cars.app.auth import require_roles, get_current_user
from cars.app.dependencies import get_async_session
from datetime import datetime


router = APIRouter(prefix="/rentals", tags=["Rent"])


def rent_days_calc(start_date: datetime, end_date: datetime) -> int:
    days = (end_date - start_date).days
    if days <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return days


@router.post("/", response_model=RentalSchema, status_code=201)
async def rent_car(
    rent_create: CreateRent,
    current_user: UserModel = Depends(require_roles("Renter", "Seller", "Admin")),
    session: AsyncSession = Depends(get_async_session),
):
    car = await session.scalar(
        select(CarModel).where(CarModel.id == rent_create.car_id, CarModel.is_active)
    )
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if car.status != CarStatus.AVAILABLE:
        raise HTTPException(status_code=400, detail="Car is not available")
    if current_user.id == car.owner_id:
        raise HTTPException(status_code=403, detail="You cannot rent your own car")

    start_date = rent_create.start_date.replace(tzinfo=None)
    end_date = rent_create.end_date.replace(tzinfo=None)

    days = rent_days_calc(start_date, end_date)
    total_price = days * car.daily_rate
    new_rental = RentalModel(
        car_id=rent_create.car_id,
        renter_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price,
        status=RentalStatus.ACTIVE,
    )
    car.status = CarStatus.RENTED
    session.add(new_rental)
    await session.commit()
    await session.refresh(new_rental)
    await session.refresh(car)

    return new_rental


@router.get("/", response_model=list[RentalSchema], status_code=200)
async def get_rentals(
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if current_user.role == "Admin":
        rentals = await session.scalars(select(RentalModel))
    elif current_user.role == "Seller":
        query = (
            select(RentalModel)
            .join(CarModel, RentalModel.car_id == CarModel.id)
            .where(CarModel.owner_id == current_user.id)
        )
        rentals = await session.scalars(query)
    elif current_user.role == "Renter":
        rentals = await session.scalars(
            select(RentalModel).where(RentalModel.renter_id == current_user.id)
        )
    return rentals.all()


@router.get("/{rental_id}", response_model=RentalSchema, status_code=200)
async def get_rent(
    rental_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    rent = await session.scalar(
        select(RentalModel)
        .where(RentalModel.id == rental_id)
        .options(selectinload(RentalModel.car))
    )
    if not rent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rent not found"
        )

    if current_user.role == "Admin":
        pass
    elif current_user.role == "Seller":
        if rent.car.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
    elif current_user.role == "Renter":
        if rent.renter_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

    return rent


@router.put("/{rental_id}/complete", response_model=RentalSchema, status_code=200)
async def change_rent(
    rental_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    rental = await session.scalar(
        select(RentalModel)
        .where(RentalModel.id == rental_id)
        .options(selectinload(RentalModel.car))
    )
    if not rental:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if current_user.role == "Admin":
        pass
    elif current_user.role == "Seller":
        if rental.car.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
    elif current_user.role == "Renter":
        if rental.renter_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

    if rental.status != RentalStatus.ACTIVE:
        raise HTTPException(
            status_code=400, detail="Only active rentals can be completed"
        )

    rental.status = RentalStatus.COMPLETED
    rental.car.status = CarStatus.AVAILABLE
    await session.commit()
    await session.refresh(rental)
    await session.refresh(rental.car)
    return rental
