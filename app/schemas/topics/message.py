import faust
from typing import AnyStr

class MessageModelChange(faust.Record, serializer='json'):
    operationType: str = ''
    fullDocument: dict = {}
    ns: dict = {}
    documentKey: dict = {}
    updateDescription: dict = {}
