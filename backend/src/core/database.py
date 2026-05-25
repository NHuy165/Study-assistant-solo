from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel, text

from backend.src.core.config import settings

if settings.DEV_MODE:
    engine = create_async_engine(str(settings.POSTGRES_URL_TEST), echo=True)
else:
    engine = create_async_engine(str(settings.POSTGRES_URL), echo=True)


async def create_database_and_tables():
    async with engine.begin() as conn:
        # Creating extensions
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))

        # Tables setup
        await conn.run_sync(SQLModel.metadata.create_all)


async def dispose():
    await engine.dispose()


async def reset_database():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session():
    async with AsyncSession(engine) as session:
        yield session
