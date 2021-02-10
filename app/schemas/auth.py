from typing import Optional
from pydantic import BaseModel, validator, AnyUrl

#Base fields for user that we can return
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None