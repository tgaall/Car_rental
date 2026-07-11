
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from config import DATABASE_URL


class Base(DeclarativeBase):
    pass


# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production (prints all SQL queries)
    future=True,
)

# Create the async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Important! Keeps objects usable after commit
)


async def get_db():
    """
    FastAPI dependency for database sessions.
    
    Usage in a route:
    @app.get("/cars")
    async def get_cars(db: AsyncSession = Depends(get_db)):
        result = await db.execute(...)
        return result.fetchall()
    """
    async with AsyncSessionLocal() as session:
        yield session