from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class ActivityCreate(BaseModel):
    pass

class ActivityUpdate(BaseModel):
    pass


class ApiEmailThread(BaseModel):
    date_created__gt: str
    date_created__lt: str

class ApiEmail(BaseModel):
    date_created__gt: str
    date_created__lt: str
