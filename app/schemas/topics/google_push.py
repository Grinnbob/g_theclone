import faust
from typing import AnyStr

class BasePushModel(faust.Record, serializer='json'):
    account: str

class PushKeyBase(faust.Record, serializer='json'):
    account: str

class PushDataModel(BasePushModel):
    payload: dict = {}
