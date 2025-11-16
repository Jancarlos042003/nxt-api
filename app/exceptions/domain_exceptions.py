class CaseNotFoundException(Exception):
    """Excepción lanzada cuando un caso no es encontrado"""

    def __init__(self, case_id: str):
        self.case_id = case_id
        super().__init__(f"El caso con ID {case_id} no existe")


class UserNotFoundException(Exception):
    """Excepción lanzada cuando un usuario no es encontrado"""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"El usuario con username {username} no existe")


class InvalidCredentialsException(Exception):
    """Excepción lanzada cuando las credenciales son inválidas"""

    def __init__(self):
        super().__init__("Credenciales inválidas")

class InvalidTokenException(Exception):
    """Excepción lanzada cuando el token JWT es inválido o ha expirado"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)