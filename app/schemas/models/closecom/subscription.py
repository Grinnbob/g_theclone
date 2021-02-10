from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class ApiSubscribeSequence(BaseModel):
    sequence_id: str
    contact_id: str
    contact_email: str
    sender_account_id: str
    sender_email: str
    sender_name: str

class SubscriptionCreate(BaseModel):
    subscription_id: str
    status: str
    data: dict

class SubscriptionUpdate(BaseModel):
    data: dict

class SubscriptionInDB(DBModelMixin):
    subscription_id: str
    status: str
    data: dict