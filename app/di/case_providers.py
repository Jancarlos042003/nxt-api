from fastapi import Depends

from app.core.db import get_dynamo_table
from app.repositories.case_repository import CaseRepository
from app.services.case_service import CaseService


def get_case_repository(table=Depends(get_dynamo_table)) -> CaseRepository:
    return CaseRepository(table)


def get_case_service(repository: CaseRepository = Depends(get_case_repository)) -> CaseService:
    return CaseService(repository)
