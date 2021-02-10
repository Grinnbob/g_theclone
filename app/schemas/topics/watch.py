import faust
from typing import AnyStr, List, Optional

class WatchKeyBase(faust.Record, serializer='json'):
    action: str #watch, stop

class WatchModel(faust.Record, serializer='json'):
    action: str
    account: str
    history_id: str = ''
    expiration: str = ''

class WatchUpdateModel(faust.Record, serializer='json'):
    action: str
    list_id: List[str]