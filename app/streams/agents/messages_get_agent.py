from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.schemas.topics.lists import ListUpdateTopicModel
from app.services.list_service import ListService
from app.services.get_request_service import RequestServiceGet
from app.services.message_service import MessageService
from app.schemas.models.gmail_req import GetReqCreate
from app.services.models.gmail_req import GetRequestModel
from app.schemas.google.gmail_api import MessagesGetRequest

from app.schemas.topics.reqres import KeyBase, GmailRequestModel
from app.streams.topics.reqres import gmail_request_topic
from app.core.config import settings
import traceback
import os

class MsgGetAgent():
    def __init__(self):
        self.app = get_stream_app()
        self.message_service = MessageService()
        self.list_service = ListService()
        self.get_request_service = RequestServiceGet()

    async def execute_list_change(self,
                                  change: ListUpdateTopicModel):
        action = change.action
        if action == 'list_created':
            pass
        elif action == 'list_updated':
            pass
        elif action == 'list_deleted':
            await self._on_list_deleted(change)
        else:
            print(f"MsgGetAgent.execute_list_change no handler for action={action} change={change}")


    async def get_requests(self,
                           status: list = [STATUS_NEW, STATUS_READY]):

        active_ids = await self.list_service.active_list_ids()

        return await self.get_request_service.get_by_status(status=status,
                                                            list_ids=active_ids)


    async def get_messages(self,
                           status: list = [STATUS_READY]):

        active_ids = await self.list_service.active_list_ids()
        return await self.message_service.get_bulk(status=status,
                                                   list_ids=active_ids)

    async def produce_task(self,
                           request: GetRequestModel):
        if request.status == STATUS_FINISHED:
            return

        try:
            params = self._serialize_params(request)
            if params:
                await gmail_request_topic.send(key=KeyBase(list_id=request.list_id),
                                               value=GmailRequestModel(
                                                   job_id=str(request['_id']),
                                                   list_id=request.list_id,
                                                   params=params,
                                                   action=params['action']
                                               ))

            return await self.get_request_service.change_status(id=str(request['_id']),
                                                                status=STATUS_IN_PROGRESS)

        except Exception as e:
            traceback.print_exc()
            print(f"{os.path.basename(__file__)} produce_task error:{str(e)}")

            return await self.get_request_service.change_status(id=str(request['_id']),
                                                                status=STATUS_ERROR,
                                                                error=str(e))

    def _serialize_params(self,
                            request: GetRequestModel):

        format = 'FULL'
        action = 'messages.get.full'
        if request.msg_format == 'FULL':
            format = 'METADATA'
            action = 'messages.get.metadata'

        params = MessagesGetRequest(
            userId=request.account,
            format=format,
            msg_ids=request.msg_ids
        )

        res = params.dict(exclude_unset=True)
        res['action'] = action

        return res


    async def produce_request(self,
                              bulk: dict):
        if not bulk:
            return

        required = bulk['_id']

        await self.message_service.update_status(status=STATUS_IN_PROGRESS,
                                                 msg_ids=bulk['msd_ids'])

        await self.get_request_service.create(body=GetReqCreate(
            account=required['account'],
            list_id=required['list_id'],
            msg_format=required['msg_format'],
            msg_ids=bulk['msg_ids']
        ))

    async def _on_list_deleted(self,
                               change: ListUpdateTopicModel):
        list_id = change.list_id
        if not list_id:
            return

        await self.get_request_service.list_delete(list_id=list_id)

        await self.message_service.list_delete(list_id=list_id)
