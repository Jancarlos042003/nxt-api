from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Annotated

from pydantic import BaseModel, Field


class CaseStatus(str, Enum):
    NUEVO = "nuevo"
    PENDIENTE = "en progreso"
    FINALIZADO = "finalizado"


class CaseCreateRequest(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=100)]
    description: Annotated[str, Field(..., min_length=10, max_length=2000)]
    status: Annotated[CaseStatus, Field(default=CaseStatus.NUEVO)]
    created_at: Annotated[datetime, Field(default_factory=lambda: datetime.now(timezone.utc))]


class CaseUpdateRequest(BaseModel):
    name: Optional[Annotated[str, Field(None, min_length=3, max_length=100)]] = None
    description: Optional[Annotated[str, Field(None, min_length=10, max_length=2000)]] = None
    status: Optional[CaseStatus] = None


class CaseResponse(BaseModel):
    id: str
    name: str
    description: str
    status: CaseStatus
    created_at: datetime
