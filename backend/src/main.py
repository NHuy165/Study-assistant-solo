from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.src.core.database import create_database_and_tables, dispose
from backend.src.exceptions.core import ExceptionCustom
from backend.src.exceptions.handlers import (
    custom_exceptions_handler,
    generic_exceptions_handler,
    starlette_exceptions_handlers,
    validation_exceptions_handler,
)
from backend.src.routes.study import router

# ----- Setting up app ----- #


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_and_tables()

    yield

    await dispose()


app = FastAPI(lifespan=lifespan)

# ----- Exception handling ----- #

app.add_exception_handler(RequestValidationError, validation_exceptions_handler)  # type: ignore
app.add_exception_handler(StarletteHTTPException, starlette_exceptions_handlers)  # type: ignore
app.add_exception_handler(ExceptionCustom, custom_exceptions_handler)  # type: ignore
app.add_exception_handler(Exception, generic_exceptions_handler)

# ----- Mounting routers ----- #

app.include_router(
    router,
    prefix="/study",
    tags=["study"],
)
