from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class AccountCreate(BaseModel):
    account_id: str
    data: dict

class AccountUpdate(BaseModel):
    data: dict

class AccountInDB(DBModelMixin):
    account_id: str
    data: dict