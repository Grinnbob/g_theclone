from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class ContactEmailCreate(BaseModel):
    email: str
    data: dict

class ContactEmailUpdate(BaseModel):
    data: dict

class ContactEmailInDB(DBModelMixin):
    email: str
    data: dict


class ApiContactsGet(BaseModel):
    skip: int = 0