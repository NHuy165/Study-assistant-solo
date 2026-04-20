from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import (
    CORSMiddleware,  # Tuấn sửa, thêm CORS do khác địa port giữa frontend và backend
)
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.src.core.database import create_database_and_tables, dispose
from backend.src.core.origins import origins
from backend.src.exceptions.core import ExceptionCustom
from backend.src.exceptions.handlers import (
    custom_exceptions_handler,
    generic_exceptions_handler,
    starlette_exceptions_handlers,
    validation_exceptions_handler,
)
from backend.src.routes import auth, document, interaction, llm_response, note, user

# ----- Setting up app ----- #


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_and_tables()

    yield

    await dispose()


app = FastAPI(lifespan=lifespan)


# Đoạn này là để test xem backend đã chạy được chưa, có thể xóa sau khi đã xác nhận backend hoạt động bình thường
# ----- Cấu hình CORS (Thêm đoạn này vào) ----- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Exception handling ----- #

app.add_exception_handler(RequestValidationError, validation_exceptions_handler)  # type: ignore
app.add_exception_handler(StarletteHTTPException, starlette_exceptions_handlers)  # type: ignore
app.add_exception_handler(ExceptionCustom, custom_exceptions_handler)  # type: ignore
app.add_exception_handler(Exception, generic_exceptions_handler)

# ----- Mounting routers ----- #

app.include_router(
    auth.router,
    prefix="",
    tags=["auth"],
)

app.include_router(
    document.router,
    prefix="/document",
    tags=["document"],
)

app.include_router(
    interaction.router,
    prefix="/interaction",
    tags=["interaction"],
)

app.include_router(
    llm_response.router,
    prefix="/llm-response",
    tags=["llm-response"],
)

app.include_router(
    note.router,
    prefix="/note",
    tags=["note"],
)

app.include_router(
    user.router,
    prefix="/user",
    tags=["user"],
)
