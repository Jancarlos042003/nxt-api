import datetime
import logging
import uuid
from typing import List

from app.exceptions.domain_exceptions import CaseNotFoundException
from app.exceptions.technical_exceptions import DatabaseException
from app.repositories.case_repository import CaseRepository
from app.schemas.case import CaseCreateRequest, CaseUpdateRequest, CaseResponse

logger = logging.getLogger(__name__)


class CaseService:
    def __init__(self, case_repository: CaseRepository):
        self.case_repository = case_repository

    def create_case(self, case_data: CaseCreateRequest) -> CaseResponse:
        """
        Crea un nuevo caso en el sistema.
        Genera un ID único y establece valores por defecto.
        """
        try:
            case_id = str(uuid.uuid4())

            # Añadir ID al diccionario para guardar
            save_dict = case_data.model_dump()
            save_dict["id"] = case_id

            self.case_repository.create_case(save_dict)

            return CaseResponse(
                id=case_id,
                name=case_data.name,
                description=case_data.description,
                status=case_data.status
            )
        except DatabaseException as e:
            logger.error(f"Error al crear el caso: {e}")
            raise  # Re-lanzar la excepción para que el manejador la capture

    def get_case(self, case_id: str) -> CaseResponse:
        """
        Obtiene un caso por su ID.
        Retorna None si no existe.
        """
        try:
            case = self.case_repository.get_case(case_id)

            # Verificar que el caso existe
            if not case:
                raise CaseNotFoundException(case_id)

            return CaseResponse(**case)
        except DatabaseException as e:
            logger.error(f"Error al obtener el caso con ID {case_id}: {e}")
            raise

    def list_cases(self) -> List[CaseResponse]:
        """
        Lista todos los casos del sistema.
        """
        try:
            cases_data = self.case_repository.list_cases()

            return [CaseResponse(**case) for case in cases_data]
        except DatabaseException as e:
            logger.error(f"Error al listar los casos: {e}")
            raise

    def update_case(self, case_id: str, case_data: CaseUpdateRequest) -> CaseResponse:
        """
        Actualiza un caso existente.
        Solo actualiza los campos proporcionados (no None).
        """
        try:
            existing_case = self.case_repository.get_case(case_id)

            # Verificar que el caso existe
            if not existing_case:
                raise CaseNotFoundException(case_id)

            # Preparar datos para actualizar (solo campos no None)
            update_data = case_data.model_dump(exclude_none=True)

            # Si no hay nada que actualizar, retornar el caso existente
            if not update_data:
                return CaseResponse(**existing_case)

            # Actualizar en repositorio
            self.case_repository.update_case(case_id, update_data)

            # Obtener el caso actualizado
            updated_case = self.case_repository.get_case(case_id)

            return CaseResponse(**updated_case)
        except DatabaseException as e:
            logger.error(f"Error al actualizar el caso con ID {case_id}: {e}")
            raise

    def delete_case(self, case_id: str) -> bool:
        """
        Elimina un caso del sistema.
        Retorna True si se eliminó.
        """
        try:
            existing_case = self.case_repository.get_case(case_id)

            # Verificar que existe antes de eliminar
            if not existing_case:
                raise CaseNotFoundException(case_id)

            self.case_repository.delete_case(case_id)

            return True
        except DatabaseException as e:
            logger.error(f"Error al eliminar el caso con ID {case_id}: {e}")
            raise
