from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from .base import DBModelMixin

class ReqBase(BaseModel):
    account: str

class ReqUpdate(BaseModel):
    status: Optional[int] = None

class ListReqCreate(ReqBase):
    list_id: str
    labels: list

class HistoryReqCreate(ReqBase):
    start_history_id: str

class WatchCreate(ReqBase):
    list_id: str
    topic_name: str
    labels: list

class GetReqCreate(ReqBase):
    list_id: str
    msg_format: str
    msg_ids: list
