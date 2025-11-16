from typing import Annotated

from fastapi import Depends

from app.core.db import get_dynamo_table_users
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def get_user_repository(table=Depends(get_dynamo_table_users)):
    return UserRepository(table)


def get_user_service(repository: Annotated[UserRepository, Depends(get_user_repository)]):
    return UserService(repository)
