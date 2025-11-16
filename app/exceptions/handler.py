from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.exceptions.domain_exceptions import CaseNotFoundException, UserNotFoundException, InvalidTokenException, \
    InvalidCredentialsException
from app.exceptions.technical_exceptions import DatabaseException


# Excepciones de dominio
async def case_not_found_handler(request: Request, exc: CaseNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": str(exc)},
    )


async def invalid_token_handler(request: Request, exc: InvalidTokenException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": str(exc)},
    )


# Excepciones técnicas
async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "Error de base de datos. Por favor, intente más tarde."},
    )


def register_handlers(app):
    app.add_exception_handler(CaseNotFoundException, case_not_found_handler)
    app.add_exception_handler(DatabaseException, database_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_handler)
    app.add_exception_handler(InvalidTokenException, invalid_token_handler)
    app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
