from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from cars.app.database import get_session_factory


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async DB session per request."""
    async with get_session_factory()() as session:
        yield session