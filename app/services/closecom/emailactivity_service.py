from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.emailactivity as emailactivity_schema
from ..models.closecom.emailactivity import CloseComEmailActivity
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class ClosecomEmailActivityService(BaseService[CloseComEmailActivity,
                                         emailactivity_schema.CloseComEmailActivityCreate,
                                         emailactivity_schema.CloseComEmailActivityUpdate]):
    def __init__(self):
        super().__init__(model=CloseComEmailActivity)

    async def upsert_many(self,
                          items: List[emailactivity_schema.CloseComEmailActivityCreate]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"items list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComEmailActivity.collection

            for item in items:
                item_dict = item.dict()

                activity_id = item_dict['activity_id']
                del item_dict['activity_id']

                res = await collection.update_one({'activity_id' : activity_id},
                                                  { '$set' : item_dict },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ClosecomEmailActivityService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def group_by_thread_id(self,
                                 date_from: str,
                                 date_to: str,
                                 customer_emails: List):
        _and = [
            {'data.date_created': {'$gt': date_from}},
            {'data.date_created': {'$lt': date_to}},
        ]

        if customer_emails:
            _and.append({
                            '$or' : [
                                    {'from_email' : {'$in' : customer_emails}},
                                    {'to_email' : {'$in' : customer_emails}}
                                ]
                            })
        pipeline = [
            {
                '$match':
                    {
                        '$and' : _and
                    }
            },
            {
                '$group':
                    {
                        '_id': '$thread_id',
                        'from_emails' : {'$push' : '$from_email'},
                        'to_emails' : {'$push' : '$to_email'},
                        'emails': {'$push': '$data'}
                    }
            },
        ]

        collection = CloseComEmailActivity.collection
        return collection.aggregate(pipeline)
