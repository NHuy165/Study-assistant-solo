from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel, text

from backend.src.core.config import settings

engine = create_async_engine(str(settings.POSTGRES_URL), echo=True)


async def create_database_and_tables():
    async with engine.begin() as conn:
        # Tạo extension
        q = text("CREATE EXTENSION IF NOT EXISTS vector;")
        await conn.execute(q)

        # Tables setup
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose():
    await engine.dispose()


async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
