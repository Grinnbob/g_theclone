import faust
from typing import AnyStr

class BaseModel(faust.Record, serializer='json'):
    job_id: str
    list_id: str
    action: str

class ParsedKeyBase(faust.Record, serializer='json'):
    action: str

class KeyBase(faust.Record, serializer='json'):
    list_id: str

class GmailRequestModel(BaseModel):
    params: dict = {}

class GmailResponseModel(BaseModel):
    payload: dict = {}
    error: bool = False

class GmailParsedResponseModel(BaseModel):
    payload: dict = {}
    error: bool = False
