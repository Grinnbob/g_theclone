from app.exceptions import *
from typing import List, Any
from .base import BaseService
import app.schemas.models.message as message_schema
from app.schemas.globals import *
from .models.message import Message
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class MessageService(BaseService[Message, message_schema.MessageCreate, message_schema.MessageUpdate]):
    def __init__(self):
        super().__init__(model=Message)

    async def get_bulk(self,
                        status: list,
                        list_ids: list = [],
                        batch_size: int = settings.MSG_BATCH_SIZE) -> Any:
        match = {
            '$match' :
                {
                    'status' : {'$in' : status}
                }
        }
        if list_ids:
            match['$match']['list_id'] = {'$in' : list_ids}

        pipeline = [
            match,
            {
                '$group':
                    {
                        '_id': {
                            'account' : '$account',
                            'msg_format' : '$msg_format',
                            'list_id' : '$list_id'
                        },
                        'msg_ids' : {'$push' : '$msg_id'}
                    }
            }
        ]

        if batch_size:
            pipeline.append({
                "$project": {
                    "msg_ids": {"$slice": ["$msg_ids", batch_size]},
                    "_id": 1
                },
            })

        return Message.aggregate(pipeline)

    async def update_status(self,
                            status: int,
                            msg_ids: list) -> Any:

        return await Message.update({'msg_id' : {'$in' : msg_ids}},
                                    {'$set' : {'status' : status}})

    async def list_delete(self,
                          list_id: str):

        return await Message.update({'list_id' : list_id}, {'$set' : {'list_id' : ''}})