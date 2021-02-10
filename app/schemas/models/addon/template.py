from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class TemplateCreate(BaseModel):
    template_id: str
    title: str
    data: dict

class TemplateUpdate(BaseModel):
    data: dict

class TemplateInDB(DBModelMixin):
    template_id: str
    title: str
    data: dict

    active: bool