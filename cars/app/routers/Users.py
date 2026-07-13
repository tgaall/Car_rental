from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from cars.app.models.User import User as UserModel
from cars.app.schemas.UserSchema import User, UserCreate, UserUpdate
from sqlalchemy import select, update
from cars.app.dependencies import get_async_session
from cars.app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    require_roles,
)
from cars.app.config import ALGORITHM, SECRET_KEY
import jwt

router = APIRouter(prefix="/users", tags=["User_data"])


@router.get("/", response_model=list[User], status_code=200)
async def get_all(session: AsyncSession = Depends(get_async_session)):
    users = await session.scalars(select(UserModel).where(UserModel.is_active))
    return users.all()


@router.post("/", response_model=User, status_code=201)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_async_session)
):

    result = await session.scalars(
        select(UserModel).where(UserModel.email == user.email)
    )
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    db_user = UserModel(
        name=user.name,
        phone=user.phone,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
    )
    session.add(db_user)
    await session.commit()
    return db_user


@router.put("/{user_id}", response_model=User, status_code=200)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_roles("Admin", "Seller", "Renter")),
):
    user = await session.scalar(
        select(UserModel).where(UserModel.id == user_id, UserModel.is_active)
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if current_user.id != user.id and current_user.role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await session.execute(
        update(UserModel)
        .where(UserModel.id == user_id)
        .values(**user_data.model_dump())
    )
    await session.commit()
    await session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=200)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(require_roles("Admin")),
):
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


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):

    result = await db.scalars(
        select(UserModel).where(UserModel.email == form_data.username)
    )
    user = result.first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh-token")
async def refresh_token(
    refresh_token: str, db: AsyncSession = Depends(get_async_session)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    result = await db.scalars(
        select(UserModel).where(UserModel.email == email, UserModel.is_active)
    )
    user = result.first()
    if user is None:
        raise credentials_exception
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
