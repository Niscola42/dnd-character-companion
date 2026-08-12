from typing import Optional

from pydantic import BaseModel

from app.domain.resource.rest import RestType


class RestRequest(BaseModel):
    rest_type: RestType


class ResourceChangeResponse(BaseModel):
    name: str
    before: int
    after: int


class HitPointChangeResponse(BaseModel):
    current_before: int
    current_after: int
    temporary_before: int
    temporary_after: int


class RestResponse(BaseModel):
    changes: list[ResourceChangeResponse]
    hit_points: Optional[HitPointChangeResponse]