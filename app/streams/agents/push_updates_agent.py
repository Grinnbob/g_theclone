from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.schemas.globals import *
from app.core.config import settings
from app.schemas.topics.google_push import PushDataModel
import traceback
from app.streams.topics.google_push import push_updates_topic
from app.providers.google.pubsub_api import PubSubApiProvider
from app.schemas.topics.google_push import PushKeyBase, PushDataModel
import base64

class PushUpdatesAgent():
    def __init__(self):
        self.app = get_stream_app()
        self.pub_sub_api = PubSubApiProvider.create_api_provider()

    async def pull(self):
        return await self.pub_sub_api.pull()

    async def ack(self,
                  ack_ids:list):
        return await self.pub_sub_api.ack(ack_ids)


    async def process_gmail_update(self,
                                   ack: str,
                                   data: str):
        try:
            update = base64.b64decode(data).decode('utf-8')

            account = update['emailAddress']

            await push_updates_topic.send(key=PushKeyBase(account=account),
                                          value=PushDataModel(payload=update))
        except Exception as e:
            print(f"process_gmail_update ERROR = {str(e)}")
            return None

        return ack