from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.subscription as subscription_schema
from ..models.closecom.subscription import CloseComSubscription
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class ClosecomSubscriptionService(BaseService[CloseComSubscription, subscription_schema.SubscriptionCreate, subscription_schema.SubscriptionUpdate]):
    def __init__(self):
        super().__init__(model=CloseComSubscription)

    async def upsert_many(self,
                          items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"itens list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComSubscription.collection

            for item in items:
                res = await collection.update_one({'subscription_id' : item['subscription_id']},
                                                  { '$set' : {
                                                      'status' : item['status'],
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ClosecomSubscriptionService.upsert_many {str(e)}  type={type(e)}")
            return None

        return res


    async def create_many(self,
                       items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"itens list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComSubscription.collection
            res = await collection.insert_many(items, ordered=False) #ordered - will ignore duplicates, but still raise an Exception
        except Exception as e:

            details = e.details
            write_errors = details.get('writeErrors', None)
            if not write_errors:
                traceback.print_exc()
                print(f"ClosecomSubscriptionService.create_many {str(e)}  type={type(e)}")
                return None

            #11000 - duplicate error is ok to pass, all other need to show
            for error in write_errors:
                if error.get('code', -100) != 11000:
                    traceback.print_exc()
                    print(error)
            return res

        return res

    async def get_grouped_by_contact(self) -> Any:
        pipeline = [
            {
                '$project':
                    {
                        'data': 1,
                        'status': 1,
                        'subscription_id': 1
                    }
            },
            {
                '$group':
                    {
                        '_id': '$data.contact_id',
                        'data': { '$push': '$data'},
                        'subscription_id' : {'$push' : '$subscription_id'},
                        'sequence_ids' : {'$push' : '$data.sequence_id'}
                    }
            },
        ]

        collection = CloseComSubscription.collection
        return collection.aggregate(pipeline)
