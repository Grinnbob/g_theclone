from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.services.list_request_service import RequestServiceList
from app.services.list_service import ListService
from app.services.models.gmail_req import ListRequestModel
from app.schemas.google.gmail_api import MessagesListRequest
from app.streams.topics.reqres import gmail_request_topic
from app.schemas.topics.reqres import GmailRequestModel, KeyBase
from app.schemas.topics.lists import ListUpdateTopicModel
from app.schemas.models.gmail_req import ListReqCreate
from app.schemas.models.list import ListLabelsChanged
from app.core.config import settings
import traceback
import os

class MsgListAgent():
    def __init__(self):
        self.app = get_stream_app()
        self.list_request_service = RequestServiceList()
        self.list_service = ListService()

    async def execute_list_change(self,
                                  change: ListUpdateTopicModel):
        action = change.action
        if action == 'list_created':
            await self._on_list_created(change)
        elif action == 'list_updated':
            await self._on_list_updated(change)
        elif action == 'list_deleted':
            await self._on_list_deleted(change)
        else:
            print(f"MsgListAgent.execute_list_change no handler for action={action} change={change}")

    async def get_requests(self,
                           status: list = [STATUS_NEW, STATUS_READY]):

        active_ids = await self.list_service.active_list_ids()

        return await self.list_request_service.get_by_status(status=status,
                                                             list_ids=active_ids)

    async def produce_task(self,
                              request: ListRequestModel):

        if self._check_finished(request):
            return await self.list_request_service.change_status(id=str(request['_id']),
                                                                 status=STATUS_FINISHED)
        try:
            params = self._serialize_params(request)
            if params:
                await gmail_request_topic.send(key=KeyBase(list_id=request.list_id),
                                               value=GmailRequestModel(
                                                   job_id=str(request['_id']),
                                                   list_id=request.list_id,
                                                   params=params,
                                                   action="messages.list"
                                               ))

            return await self.list_request_service.change_status(id=str(request['_id']),
                                                                 status=STATUS_IN_PROGRESS)

        except Exception as e:
            traceback.print_exc()
            print(f"{os.path.basename(__file__)} produce_task error:{str(e)}")

            return await self.list_request_service.change_status(id=str(request['_id']),
                                                                 status=STATUS_ERROR,
                                                                 error=str(e))


    async def _on_list_created(self,
                               change: ListUpdateTopicModel):
        labels_changed = change.labels_changed
        if not labels_changed:
            return

        list_id = change.list_id
        accounts_labels = self._parse_labels(labels_changed)

        if accounts_labels:
            return await self._create_list_requests(list_id=list_id,
                                                    labels=accounts_labels)

    async def _on_list_updated(self,
                               change: ListUpdateTopicModel):
        labels_changed = change.labels_changed
        if not labels_changed:
            return

        list_id = change.list_id
        accounts_labels = self._parse_labels(labels_changed)

        if accounts_labels:
            return await self._create_list_requests(list_id=list_id,
                                                    labels=accounts_labels)


    async def _on_list_deleted(self,
                               change: ListUpdateTopicModel):
        list_id = change.list_id
        if not list_id:
            return

        await self.list_request_service.list_delete(list_id=list_id)



    def _serialize_params(self,
                            request: ListRequestModel):


        params = MessagesListRequest(
            userId=request.account,
            labelIds=request.labels
        )

        if request.next_page_token:
            params.pageToken = request.next_page_token

        return params.dict(exclude_unset=True)

    def _check_finished(self,
                        request: ListRequestModel):

        if request.status == STATUS_READY:
            if not request.next_page_token:
                return True

        return False

    def _parse_labels(self,
                      labels_changed: ListLabelsChanged):

        if not labels_changed:
            return {}

        return labels_changed.get('added', {})


    async def _create_list_requests(self,
                              list_id: str,
                              labels: dict):

        items =[]
        for account, labels in labels.items():
            if not account or not labels:
                print(f"WARNING: MsgListAgent._create_list_requests strange behavor account={account} labels={labels} for change={list_id}")
                continue

            items.append(ListReqCreate(
                list_id=list_id,
                account=account,
                labels=labels
            ))

        if items:
            await self.list_request_service.create_many(items=items)