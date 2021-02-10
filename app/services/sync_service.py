from app.exceptions import *
from typing import List, Any
from .base import BaseService
import app.schemas.models.gmail_req as sync_schema
from app.schemas.globals import *
from .models.gmail_req import SyncLabel, SyncJob
from .models.message import Message
from app.core.config import settings
from bson.objectid import ObjectId
import traceback

class SyncService(BaseService[SyncLabel, sync_schema.SyncCreate, sync_schema.SyncUpdate]):
    def __init__(self):
        super().__init__(model=SyncLabel)


    async def add_many(self,
                       syncs: List[sync_schema.SyncBase]) -> Any:
        res = None
        if not syncs:
            raise AppErrors(f"syncs list can't be empty")

        try:
            res = await SyncLabel.insert_many(syncs, ordered=False) #ordered - will ignore duplicates, but still raise an Exception
        except Exception as e:
            #TODO: catch only duplicate error
            traceback.print_exc()
            print(f"SyncService.add_many {str(e)}  type={type(e)}")
            return None

        return res

    async def remove_job(self,
                         id: ObjectId) -> Any:

        exist = await SyncJob.find_one({'_id' : id})
        if not exist:
            raise AppErrors(f"Job Not exist {id}")

        await exist.remove()

        return True

    async def on_job_deleted(self,
                             job_id: ObjectId,
                             labels_ids: list) -> Any:

        return await SyncLabel.update({'label_id' : {'$in' : labels_ids}, 'sync_job_id' : job_id},
                                      {'$set' : {
                                          'status' : STATUS_DELETED,
                                          'sync_job_id' : None
                                      }})

    async def delete_job(self,
                         job_id: ObjectId,
                         labels_ids: list) -> Any:
        job = await SyncJob.find_one({'_id': job_id})
        if not job:
            raise AppErrors(f"Job Not exist {job_id}")

        ids = job.labels_ids.to_mongo()
        if not ids:
            await job.remove()
            return True

        updated_ids = [x for x in ids if x not in labels_ids]
        if not updated_ids:
            await job.remove()
            return True

        job.labels_ids = updated_ids
        await job.commit()
        await job.reload()

        return job

    async def create_msg_batch_job(self,
                                   batch: dict,
                                   action: str = 'messages.get') -> SyncJob:
        data = {
            'msg_ids' : batch['msg_ids']
        }
        new_job = SyncJob(
            list_id=batch['list_id'],
            account=batch['_id'],
            data=data,

            status=STATUS_NEW,
            action=action,
        )

        await new_job.commit()
        await new_job.reload()

        return new_job

    async def create_list_job(self,
                         item: dict,
                         action: str = 'messages.list') -> SyncJob:

        new_job = SyncJob(
            list_id=item['list_id'],
            account=item['_id'],
            labels_ids=item['labels_ids'],

            status=STATUS_NEW,
            action=action,
        )

        await new_job.commit()
        await new_job.reload()

        return new_job

    async def on_msg_batch_job_created(self,
                                       batch:dict,
                                       job_id: ObjectId) -> Any:
        msg_ids = batch['msg_ids']
        if not msg_ids:
            raise AppErrors(f"on_msg_batch_job_created ERROR: Can't update empty msg_ids={msg_ids}")

        return await Message.update({'msg_id' : {'$in' : msg_ids}},
                                      {'$set' : {
                                          'status' : STATUS_IN_PROGRESS,
                                          'sync_job_id' : job_id
                                      }})

    async def on_job_created(self,
                             item: dict,
                             job_id: ObjectId) -> Any:
        labels_ids = item['labels_ids']
        if not labels_ids:
            raise AppErrors(f"on_job_created ERROR: Can't update empty ids={ids}")

        return await SyncLabel.update({'label_id' : {'$in' : labels_ids}},
                                      {'$set' : {
                                          'status' : STATUS_IN_PROGRESS,
                                          'sync_job_id' : job_id
                                      }})

    async def update_list_status(self,
                                list_id: str,
                                status: int) -> Any:

        return await SyncLabel.update({'list_id' : list_id}, {'$set' : {'status' : status}})

    async def get_grouped_by_job(self,
                                 status: list) -> Any:
        pipeline = [
            {
                '$match' :
                    {
                        'status' : {'$in' : status},
                        'sync_job_id' : {'$ne' : None}
                    }
            },
            {
                '$group':
                    {
                        '_id': 'sync_job_id',
                        'accounts': { '$push': '$account'},
                        'labels_ids' : {'$push' : '$label_id'},
                        'list_id' : '$list_id'
                    }
            }
        ]

        return SyncLabel.aggregate(pipeline)

    async def get_grouped_by_account(self,
                                    status: list,
                                    sync_job_exist: bool = False,
                                    accounts: list = None) -> Any:
        match = {
            '$match' :
                {
                    'status' : {'$in' : status}
                }
        }

        if  sync_job_exist:
            match['$match']['sync_job_id'] = {'$ne' : None}
        else:
            match['$match']['sync_job_id'] = None

        if accounts:
            match['$match']['account'] = {'$in' : accounts}

        pipeline = [
            match,
            {
                '$group':
                    {
                        '_id': '$account',
                        'labels_ids' : {'$push' : '$label_id'},
                        'list_id' : '$list_id'
                    }
            }
        ]

        return SyncLabel.aggregate(pipeline)

    async def get_by_status(self,
                            status: list) -> Any:

        return SyncLabel.find({'status' : {'$in' : status}})

