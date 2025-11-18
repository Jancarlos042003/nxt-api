from datetime import datetime, timedelta, UTC
from typing import Optional, Annotated

from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.di.user_provider import get_user_service
from app.exceptions.domain_exceptions import InvalidTokenException

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


# FUNCIONES JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera un token de acceso JWT."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Generamos el token
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# DEPENDENCIAS DE FASTAPI
def get_current_user(token: Annotated[str | None, Cookie()] = None, user_service=Depends(get_user_service)):
    """Obtiene el usuario actual a partir del token JWT."""
    try:
        # Decodificamos el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise InvalidTokenException("Token inválido")

    except JWTError:
        raise InvalidTokenException("Token inválido o expirado")

    user = user_service.get_user(username)

    return user
