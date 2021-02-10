from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class CloseComCustomerStatCreate(BaseModel):
    pass

class CloseComCustomerStatUpdate(BaseModel):
    pass
