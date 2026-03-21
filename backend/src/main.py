from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.src.core.database import create_database_and_tables, dispose
from backend.src.routes.study import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_and_tables()

    yield

    await dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(
    router,
    prefix="/study",
    tags=["study"],
)
