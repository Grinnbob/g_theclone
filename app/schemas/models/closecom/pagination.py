from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin


class CloseComPaginationCreate(BaseModel):
    endpoint: str

class CloseComPaginationUpdate(BaseModel):
    pass