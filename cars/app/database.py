from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from cars.app.config import DATABASE_URL

class Base(DeclarativeBase):
    pass

# Lazy load engine - don't create on import
_engine = None
_AsyncSessionLocal = None

def get_engine():
    """Lazy load the async engine"""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            DATABASE_URL,
            echo=True,
            future=True,
        )
    return _engine

def get_session_factory():
    """Lazy load the session factory"""
    global _AsyncSessionLocal
    if _AsyncSessionLocal is None:
        _AsyncSessionLocal = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _AsyncSessionLocal

async def get_db():
    """FastAPI dependency for database sessions"""
    async with get_session_factory()() as session:
        yield session