from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from .base import DBModelMixin

class AccountBase(BaseModel):
    email: str
    owner_id: ObjectId = None
    credentials: Optional[dict] = None

    class Config:
        arbitrary_types_allowed = True

class AccountCreate(AccountBase):
    is_logged: int = 0

class AccountUpdate(AccountBase):
    pass

class AccountInDB(DBModelMixin):
    owner_id: Any = Field(default='', alias="owner_id")
    email: str
    credentials: dict = {}
    status: int
    error_message: str = ''

    @validator("owner_id")
    def validate_owner_id(cls, owner_id):
        return str(owner_id)