from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class TestCreate(BaseModel):
    email: EmailStr
    title: str
    data: dict

class TestUpdate(BaseModel):
    data: dict

class TestInDB(DBModelMixin):
    user_id: Any = Field(..., alias="user_id")
    title: str
    data: dict

    active: bool

    @validator("user_id")
    def validate_user_id(cls, user_id):
        return str(user_id)