from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.core.config import settings
import traceback

from app.schemas.topics.lists import ListDataTopicModel, ListKeyBaseModel
from app.schemas.topics.message import MessageModelChange
from app.streams.topics.lists import list_data_topic

class MsgModelUpdateAgent():
    def __init__(self):
        self.app = get_stream_app()

    async def execute_message_change(self,
                                     change: MessageModelChange):
        action = change.operationType

        if action == 'insert':
            await self._on_insert(change)
        elif action == 'update':
            await self._on_update(change)
        elif action == 'delete':
            await self._on_delete(change)
        elif action == 'drop':
            await self._on_drop(change)
        else:
            raise AppErrors(f"Unknow action={action} for change={change}")


    async def _on_update(self,
                         change: MessageModelChange):
        document = change.fullDocument
        if not document:
            return

        msg_id = document.get('msg_id')

        merge = self._parse_updates(change.updateDescription)
        if merge:
            return await self.produce_changes(merge)



    async def _on_delete(self,
                         change: MessageModelChange):
        pass


    async def _on_insert(self,
                         change: MessageModelChange):
        pass

    async def _on_drop(self,
                         change: MessageModelChange):
        pass


    def _parse_updates(self,
                       update_description: dict):
        if not update_description:
            return {}

        fields_updated = update_description.get('updatedFields', None)
        if not fields_updated:
            return {}

        return fields_updated.get('merge', {})

    async def produce_changes(self,
                              merge: dict):
        if not merge:
            return

        action = merge['action']

        if action == 'new_data':
            await self._generate_add_data(merge)

        elif action == 'deleted_data':

            list_id = merge['list_id']
            email = merge['email']

            await self._generate_delete_data(list_id=list_id,
                                             email=email)
        elif action == 'list_changed':
            old_list_id = merge['old_list_id']
            email = merge['email']

            await self._generate_delete_data(list_id=old_list_id,
                                             email=email)
            await self._generate_add_data(merge)
        else:
            print(f"Unknown merge action={action} for merge={merge}")

        return

    async def _generate_add_data(self,
                                 merge: dict):

        if not merge:
            return

        list_id = merge['list_id']
        if list_id:
            raise AppErrors(f"_generate_add_data merge[list_id] can't be empty merge={merge}")

        return await list_data_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                          value=ListDataTopicModel(
                                              action='add_data',
                                              list_id=list_id,
                                              email=merge['email'],
                                              incoming=merge['incoming']
                                          ))

    async def _generate_delete_data(self,
                                list_id: str,
                                email: str):


        return await list_data_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                          value=ListDataTopicModel(
                                              action='delete_data',
                                              list_id=list_id,
                                              email=email
                                          ))