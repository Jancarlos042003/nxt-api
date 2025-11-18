from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.core.security import create_access_token, get_current_user
from app.di.user_provider import get_user_service
from app.exceptions.domain_exceptions import InvalidCredentialsException

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@auth_router.post("/login")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                user_service=Depends(get_user_service)):
    username = form_data.username
    password = form_data.password

    # Obtener usuario
    user = user_service.get_user(username)

    # Verificar contraseña
    if not pwd_context.verify(password, user["password"]):
        raise InvalidCredentialsException

    # Creamos el payload del token
    data = {
        "sub": user["username"],
        "name": user["name"],
    }

    token = create_access_token(data)

    return {"token": token, "user": {"username": user["username"], "name": user["name"]}}


@auth_router.get("/me")
def get_profile(user: Annotated[dict, Depends(get_current_user)]):
    return {"username": user["username"], "name": user["name"]}
