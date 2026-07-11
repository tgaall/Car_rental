from fastapi import FastAPI
from contextlib import asynccontextmanager
from cars.app.database import get_engine
from cars.app.routers.Car import router as car_router
from cars.app.routers.Users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    _ = get_engine()
    yield
    engine = get_engine()
    await engine.dispose()


app = FastAPI(
    title="Car rental",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(car_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Welcome to car rental utility"}
