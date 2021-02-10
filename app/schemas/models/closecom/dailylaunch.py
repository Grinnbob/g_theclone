from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin


class DailyLaunchCreate(BaseModel):
    sequence_id: str
    smartview_id: str
    data: dict

class DailyLaunchUpdate(BaseModel):
    data: dict

class DailyLaunchInDB(DBModelMixin):
    sequence_id: str
    smartview_id: str
    data: dict