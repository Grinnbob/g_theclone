from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, AnyUrl, Field


class DBModelMixin(BaseModel):
    id: Optional[Any] = Field(..., alias="_id")

    @validator("id")
    def validate_id(cls, id):
        return str(id)

    class Config:
        arbitrary_types_allowed = True
