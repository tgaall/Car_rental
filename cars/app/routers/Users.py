from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from cars.app.models.User import User as UserModel
from cars.app.schemas.UserSchema import User, UserCreate
from sqlalchemy import select, update
from cars.app.dependencies import get_async_session

router = APIRouter(prefix="/users", tags=["User_data"])


@router.get("/", response_model=list[User], status_code=200)
async def get_everybody(session: AsyncSession = Depends(get_async_session)):
    users = await session.scalars(select(UserModel).where(UserModel.is_active))
    return users.all()


@router.get("/{user_id}", response_model=User, status_code=200)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.scalar(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active)
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post("/", response_model=User, status_code=201)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    session_user = UserModel(**user.model_dump())
    session.add(session_user)
    await session.commit()
    return session_user


@router.put("/{user_id}", response_model=User, status_code=200)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    user = await session.scalar(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active)
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await session.execute(
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(**user_data.model_dump())
    )
    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await session.scalar(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active)
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await session.execute(
        update(UserModel).where(UserModel.id == user_id).values(is_active=False)
    )
    await session.commit()
    await session.refresh(user)
    return {"message": "success"}
