from fastapi import FastAPI
from contextlib import asynccontextmanager
from cars.app.database import get_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    _ = get_engine()
    yield
    # Shutdown
    engine = get_engine()
    await engine.dispose()

app = FastAPI(
    title="Car rental",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/")
async def root():
    return {"message": "Welcome to car rental utility"}