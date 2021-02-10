from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class CloseComEmailActivityCreate(BaseModel):
    activity_id: str
    thread_id: str
    from_email: str
    to_email: str
    direction:str

    data: dict

class CloseComEmailActivityUpdate(BaseModel):
    pass

class ApiGetEmailActivity(BaseModel):
    date_created__gt: str
    date_created__lt: str