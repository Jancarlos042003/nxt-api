import logging

from app.exceptions.domain_exceptions import UserNotFoundException
from app.exceptions.technical_exceptions import DatabaseException
from app.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, username: str):
        """
        Obtiene un usuario por su nombre de usuario.
        """
        try:
            user = self.user_repository.get_user(username)

            if not user:
                raise UserNotFoundException(username)

            return user
        except DatabaseException as e:
            logger.error(f"Error al obtener el usuario con username {username}: {e}")
            raise
