from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from .base import DBModelMixin

class ListCreate(BaseModel):
    pass

class ListUpdate(BaseModel):
    pass

class ListLabelsChanged(BaseModel):
    added: dict
    removed: dict

class ListInDB(DBModelMixin):
    owner_id: Optional[Any] = Field(..., alias="owner_id")
    title: str
    filter: List

    tags: Optional[List] = None
    export_url: Optional[AnyUrl] = None

    @validator("owner_id")
    def validate_owner_id(cls, owner_id):
        return str(owner_id)