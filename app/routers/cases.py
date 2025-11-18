import logging

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_user
from app.di.case_providers import get_case_service
from app.schemas.case import CaseCreateRequest, CaseUpdateRequest
from app.services.case_service import CaseService

logger = logging.getLogger(__name__)

cases_router = APIRouter(dependencies=[Depends(get_current_user)])


@cases_router.post("/create", status_code=status.HTTP_201_CREATED)
def create_case(case: CaseCreateRequest, service: CaseService = Depends(get_case_service)):
    return service.create_case(case)


@cases_router.get("/{case_id}")
def get_case(case_id: str, service: CaseService = Depends(get_case_service)):
    return service.get_case(case_id)


@cases_router.put("/{case_id}")
def update_case(case_id: str, case: CaseUpdateRequest, service: CaseService = Depends(get_case_service)):
    return service.update_case(case_id, case)


@cases_router.get("")
def list_cases(service: CaseService = Depends(get_case_service)):
    return service.list_cases()


@cases_router.delete("/{case_id}")
def delete_case(case_id: str, service: CaseService = Depends(get_case_service)):
    service.delete_case(case_id)
    return {"message": "Caso eliminado exitosamente"}
