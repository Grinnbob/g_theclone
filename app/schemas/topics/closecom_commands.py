import faust
from typing import AnyStr
class CloseCommandKey(faust.Record, serializer='json'):
    command: str

class CloseCommandModel(faust.Record, serializer='json'):
    command: str
    payload: dict