from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from .base import DBModelMixin

class AdmAccountChangeStatus(BaseModel):
    account_id: str
    active: bool


class AdmAccountConnect(BaseModel):
    account_id: str
    user_id: str




class AdmTemplateEdit(BaseModel):
    template_id: str
    data: dict


class AdmTemplateChangeStatus(BaseModel):
    template_id: str
    active: bool

class AdmTemplateConnect(BaseModel):
    template_id: str
    account_ids: List[str] = []
    all: bool = False



class AdmSequenceEdit(BaseModel):
    sequence_id: str
    data: dict


class AdmSequenceChangeStatus(BaseModel):
    sequence_id: str
    active: bool




class AdmUserChangeLevel(BaseModel):
    user_id: str
    level: int

