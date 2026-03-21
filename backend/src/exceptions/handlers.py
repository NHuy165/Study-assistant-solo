from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.src.exceptions.core import (
    ExceptionCustom,
    ExceptionResponse,
    ExceptionType,
)


async def custom_exceptions_handler(request: Request, exc: ExceptionCustom):
    exception_response = ExceptionResponse(
        exception_type=exc.exception_type,
        message=exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exception_response.model_dump(),
        headers=exc.headers,
    )


async def starlette_exceptions_handlers(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        exception_type = ExceptionType.NOT_FOUND
    elif exc.status_code == 405:
        exception_type = ExceptionType.METHOD

    # Just to be safe. Realistically never gonna happen.
    else:
        exception_type = ExceptionType.REQUEST

    exception_response = ExceptionResponse(
        exception_type=exception_type, message=str(exc.detail)
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=exception_response.model_dump(),
        headers=exc.headers,
    )


async def validation_exceptions_handler(request: Request, exc: RequestValidationError):
    exception_response = ExceptionResponse(
        exception_type=ExceptionType.REQUEST,
        message="Request validation error.",
    )

    return JSONResponse(status_code=400, content=exception_response.model_dump())


async def generic_exceptions_handler(request: Request, exc: Exception):
    exception_response = ExceptionResponse(
        exception_type=ExceptionType.INTERNAL_ERROR,
        message="Internal server error.",
    )

    return JSONResponse(
        status_code=500,
        content=exception_response.model_dump(),
    )
