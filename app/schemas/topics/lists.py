import faust
from typing import AnyStr

class ListKeyBaseModel(faust.Record, serializer='json'):
    list_id: str

class ListModelChange(faust.Record, serializer='json'):
    operationType: str = ''
    fullDocument: dict = {}
    ns: dict = {}
    documentKey: dict = {}
    updateDescription: dict = {}


class ListDataTopicModel(faust.Record, serializer='json'):
    action: str
    list_id: AnyStr
    email: str = ''
    subject: str = ''
    labels: str = ''
    incoming: int = 0

class ListUpdateTopicModel(faust.Record, serializer='json'):
    list_id: str
    labels_changed: dict
    action: str

