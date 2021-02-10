from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field
from bson.objectid import ObjectId
from ..base import DBModelMixin

class RankSdrDialogCreate(BaseModel):
    pass

class RankSdrDialogUpdate(BaseModel):
    pass
