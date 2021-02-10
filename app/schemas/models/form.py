from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from .base import DBModelMixin

class FormCreate(BaseModel):
    pass

class FormUpdate(BaseModel):
    form_id: str
    step: str
    data: dict

class FormInDB(DBModelMixin):
    owner_id: Any = Field(..., alias="owner_id")
    form_id: str
    data: Optional[dict] = None

    @validator("owner_id")
    def validate_owner_id(cls, owner_id):
        return str(owner_id)
