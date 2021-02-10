from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.schemas.models.list import ListLabelsChanged
from app.schemas.topics.lists import ListModelChange, ListDataTopicModel, ListUpdateTopicModel, ListKeyBaseModel
from app.streams.topics.lists import list_data_topic, list_update_topic
from faust.topics import Topic

class ListModelUpdateAgent():
    def __init__(self):
        self.app = get_stream_app()

    async def execute_list_change(self, change: ListModelChange):
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

    async def _on_insert(self, change: ListModelChange):
        document = change.fullDocument
        if not document:
            return

        list_id = document.get('_id').get('$oid')

        labels_changed = self.create_labels_changes(document)

        await list_data_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                   value=ListDataTopicModel(action="insert",
                                                            list_id=list_id))
        if labels_changed:
            await list_update_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                         value=ListUpdateTopicModel(
                                                     list_id=list_id,
                                                     labels_changed=labels_changed,
                                                     action='list_created'
                                                 ))


    async def _on_delete(self, change: ListModelChange):
        document = change.documentKey
        if not document:
            return

        list_id = document.get('_id').get('$oid')

        await list_data_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                   value=ListDataTopicModel(action="delete",
                                                            list_id=str(list_id)))

        await list_update_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                     value=ListUpdateTopicModel(
                                                 list_id=list_id,
                                                 labels_changed={},
                                                 action='list_deleted'
                                             ))

    async def _on_update(self, change):
        document = change.fullDocument
        if not document:
            return

        list_id = document.get('_id').get('$oid')

        labels_changed = self.parse_labels_changes(change.updateDescription)
        if labels_changed:
            await list_update_topic.send(key=ListKeyBaseModel(list_id=list_id),
                                         value=ListUpdateTopicModel(
                                                     list_id=list_id,
                                                     labels_changed=labels_changed,
                                                     action='list_updated'
                                                 ))


    async def _on_drop(self, change):
        #TODO: implement actions on FULL Collection change
        #drop - fires when you drop a collection
        #delete - fires when you remove a document
        pass

    def create_labels_changes(self, document):
        if not document:
            return {}

        account_labels = document.get('account_labels', None)
        if not account_labels:
            raise AppErrors(f"create_labels_changes ERROR: there is no account_labels for document:{document}")

        changes = ListLabelsChanged(
            added=account_labels,
            removed= {}
        )

        return changes.dict()


    def parse_labels_changes(self, update_description):
        if not update_description:
            return {}

        fields_updated = update_description.get('updatedFields', None)
        if not fields_updated:
            return {}

        return fields_updated.get('labels_changed', {})