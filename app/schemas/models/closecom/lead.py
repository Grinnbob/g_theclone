from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin


class CloseComLeadCreate(BaseModel):
    lead_id: str
    customer: str
    status_id: str
    status_label: str

    data: dict


class CloseComLeadUpdate(BaseModel):
    pass

class CloseComLeadChangeStatus(BaseModel):
    lead_id: str
    status_id: str


class ApiLeadChangeStatus(BaseModel):
    status_id: str

class ApiGetLeads(BaseModel):
    query: str