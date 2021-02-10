from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from .base import DBModelMixin

class MessageBase(BaseModel):
    account: str


class MessageCreate(BaseModel):
    msg_id: str
    msg_format: str #meta, full

class MessageUpdate(BaseModel):
    pass


class MessageInDB(MessageBase):
    status: int = 0
    raw_message: dict = None
