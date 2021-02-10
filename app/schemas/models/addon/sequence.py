from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin


class SequenceCreate(BaseModel):
    sequence_id: str
    title: str
    data: dict

class SequenceUpdate(BaseModel):
    data: dict

class SequnceInDB(DBModelMixin):
    sequence_id: str
    title: str
    data: dict

    active: bool