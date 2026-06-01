import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from backend.src.core.config import settings
from backend.src.core.database import get_async_session
from backend.src.main import FastAPI, app

# ----- TEST CONFIGURATIONS ----- #

engine = create_async_engine(
    str(settings.POSTGRES_URL_TEST),
    echo=True,
    pool_size=20,
    max_overflow=60,
    pool_timeout=30.0,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(name="session")
async def session_fixture():
    # Setup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Yield session
    async with SessionLocal() as session:
        yield session

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(name="app")
async def app_fixture(session: AsyncSession):
    app.dependency_overrides[get_async_session] = lambda: session

    yield app

    app.dependency_overrides.clear()


@pytest.fixture(name="client")
async def client_fixture(app: FastAPI):
    transport = ASGITransport(app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
