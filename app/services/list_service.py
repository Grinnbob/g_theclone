from typing import Any
from app.schemas.globals import *
from app.exceptions import *
from .base import BaseService
import app.schemas.models.list as list_schema
from .models.list import SyncList
from app.core.config import settings
from bson.objectid import ObjectId


class ListService(BaseService[SyncList, list_schema.ListCreate, list_schema.ListUpdate]):
    def __init__(self):
        super().__init__(model=SyncList)

    async def change_labels(self,
                            id: ObjectId,
                            actions: list_schema.ListLabelsChanged) -> SyncList:
        exist = await SyncList.find_one({'_id' : id})
        if not exist:
            raise AppErrors(f"List doesn't exist {id}")

        exist['labels_changed'] = actions.dict()

        await exist.commit()
        await exist.reload()

        return exist


    async def change_status(self,
                            id: ObjectId,
                            status: int) -> Any:

        return await SyncList.update_one({'_id' : id},
                                         {'$set' : {'status' : status}})


    async def pause(self,
                    id: ObjectId,
                    status: int = STATUS_PAUSED) -> Any:

        return await self.change_status(id=id,
                                        status=status)


    async def run(self,
                  id: ObjectId,
                  status: int = STATUS_IN_PROGRESS) -> Any:

        return await self.change_status(id=id,
                                        status=status)

    async def active_list_ids(self,
                              status: int = STATUS_IN_PROGRESS,
                              limit: int = settings.MAX_ACTIVE_LISTS):

        cursor = SyncList.find({'status' : status}).limit(limit)

        items = list(await cursor.to_list(length=limit))

        return [l['_id'] for l in items]