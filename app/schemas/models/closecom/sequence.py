from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin


class CloseComSequenceCreate(BaseModel):
    sequence_id: str
    data: dict

class CloseComSequenceUpdate(BaseModel):
    data: dict


class CloseComSequenceInDB(DBModelMixin):
    sequence_id: str
    data: dict

class BulkStartSequence(BaseModel):
    query: str
    sequence_id: str
    sender_account_id: str
    sender_name: str
    sender_email: str
    action_type: str = "subscribe"
    contact_preference: str = "lead"

class BulkPauseSequence(BaseModel):
    action_type: str = "pause"
    sequence_id: str

class BulkResumeSequence(BaseModel):
    action_type: str = "resume"
    sequence_id: str

class EditSubscription(BaseModel):
    status: str
