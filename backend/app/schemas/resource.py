from typing import Any

from pydantic import BaseModel, Field

from app.domain.resource.resource import RecoveryType


class ResourceCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    source: str = Field(min_length=1, max_length=100)
    maximum: int = Field(gt=0)
    current: int = Field(ge=0)
    recovery_type: RecoveryType
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class ResourceResponse(BaseModel):
    id: int
    character_id: int
    name: str
    source: str
    maximum: int
    current: int
    recovery_type: RecoveryType
    metadata: dict[str, Any]

class ResourceAmountRequest(BaseModel):
    amount: int = Field(ge=0)