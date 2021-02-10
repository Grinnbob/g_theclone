from typing import Optional, Any, List, Type, TypeVar, Union
from app.exceptions import *
from ..base import BaseService
import app.schemas.models.closecom.dailylaunch as dailylaunch_schema
from ..models.closecom.dailylaunch import CloseComDailyLaunch, CloseComSmartView
from aiogoogle import Aiogoogle
from app.core.config import settings
from bson.objectid import ObjectId
import traceback
from datetime import datetime
from datetime import timedelta
import arrow

class ClosecomDailyLaunchService(BaseService[CloseComDailyLaunch,
                                             dailylaunch_schema.DailyLaunchCreate,
                                             dailylaunch_schema.DailyLaunchUpdate]):
    def __init__(self):
        super().__init__(model=CloseComDailyLaunch)

    async def update_data(self,
                          id: str,
                          data: dict):

        collection = CloseComDailyLaunch.collection
        return await collection.update_one({'_id': ObjectId(id)},
                                          {'$set': {
                                              'data': data
                                            }
                                          })

    async def get_launch_for_today(self,
                                   smartview_id:str,
                                   sequence_id:str) -> Any:
        today = datetime.utcnow()
        current_day = str(today.date())

        return await CloseComDailyLaunch.find_one({'sequence_id' : sequence_id,
                                            'smartview_id' : smartview_id,
                                            'created_day' : {'$eq' : current_day}})


    async def launch(self, payload: dailylaunch_schema.DailyLaunchCreate) -> Any:
        today = datetime.utcnow()
        current_day = str(today.date())

        exist = await CloseComDailyLaunch.find_one({'sequence_id' : payload.sequence_id,
                                            'smartview_id' : payload.smartview_id,
                                            'data' : {'$ne' : None},
                                            'created_day' : {'$eq' : current_day}})
        if exist:
            error = f"ClosecomDailyLaunchService.launch ERROR You already launch sequence_id={payload.sequence_id} for samrtview_id={payload.smartview_id} today={date}"
            raise AppErrors(error)

        if not payload.data:
            raise AppErrors("ClosecomDailyLaunchService.launch ERROR: payload.data can't be empty")

        data = payload.dict()
        data['created_day'] = current_day

        new_launch = CloseComDailyLaunch(**data)

        await new_launch.commit()
        await new_launch.reload()

        return new_launch

    async def can_launch(self, payload: dailylaunch_schema.DailyLaunchCreate) -> Any:
        today = datetime.utcnow()
        current_day = str(today.date())

        exist = await CloseComDailyLaunch.find_one({'sequence_id' : payload.sequence_id,
                                            'smartview_id' : payload.smartview_id,
                                            'data' : {'$ne' : None},
                                            'created_day' : {'$eq' : current_day}})

        if exist:
            return False

        return True

    async def smartview_upsert_many(self,
                                    items: List[dict]) -> Any:
        res = None
        if not items:
            raise AppErrors(f"itens list can't be empty")

        try:
            #low level operations start here because of poor implamentation of umongo
            collection = CloseComSmartView.collection

            for item in items:
                res = await collection.update_one({'smartview_id' : item['smartview_id']},
                                                  { '$set' : {
                                                      'data' : item['data']
                                                    }
                                                  },
                                                  upsert=True)
        except Exception as e:
            traceback.print_exc()
            print(f"ClosecomDailyLaunchService.smartview_upsert_many {str(e)}  type={type(e)}")
            return None

        return res

    async def get_smartview_query(self, smartview_id) -> Any:
        exist = await CloseComSmartView.find_one({'smartview_id' : smartview_id})
        if not exist:
            raise AppErrors(f"ClosecomDailyLaunchService.get_smartview_query ERROR: {smartview_id} didn't find in a database")

        data = exist.data

        return data.get('query', None)


    async def smartview_id_to_name(self):
        cursor = CloseComSmartView.find()

        all_smartviews = {}
        async for sm in cursor:
            all_smartviews[sm.smartview_id] = sm.data.get('name')

        return all_smartviews


    async def filter_by_date(self, created_day):
        pipeline = [
            {
                '$match':
                    {
                        'created_day': created_day,
                    }
            },
            {
                '$group':
                    {
                        '_id': {
                            'smartview_id': '$smartview_id',
                            'sequence_id': '$sequence_id'
                        },
                        'contacts': {'$push': '$data'}
                    }
            },
        ]

        collection = CloseComDailyLaunch.collection
        return collection.aggregate(pipeline)
