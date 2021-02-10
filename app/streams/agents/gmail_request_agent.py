from typing import Any
from app.exceptions import *
from app.streams import get_stream_app
from app.services.account_service import AccountService
from app.schemas.globals import *
from app.schemas.topics.reqres import GmailRequestModel, GmailResponseModel, KeyBase
from app.providers.google.gmail_api import GmailApiProvider

from app.streams.topics.reqres import gmail_response_topic

from app.core.config import settings

import traceback

class GmailRequestAgent():
    def __init__(self):
        self.app = get_stream_app()
        self.account_service = AccountService()

    async def execute_request(self,
                              req: GmailRequestModel) -> Any:
        action = req.action

        if action == 'messages.list':
            return await self._on_messages_list(req)
        elif action == 'message.get':
            return await self._on_messages_get(req)
        else:
            raise AppErrors(f"execute_request unknown action={action}")

        return

    async def _on_messages_list(self,
                               req: GmailRequestModel) -> Any:

        body = req.body
        if not body:
            raise AppErrors(f"_on_messages_list ERROR: body can't be empty for req={req}")

        email = body['account']
        if not email:
            raise AppErrors(f"_on_messages_list ERROR: account can't be empty for req={req}")

        labels_ids = body['labels_ids']
        if not labels_ids:
            raise AppErrors(f"_on_messages_list ERROR: labels_ids can't be empty for req={req}")

        account = self.get_account(email)

        gmail_api = await GmailApiProvider.create_api_provider(user_creds=account.credentials)

        next_page_token = body.get('next_page_token', None)
        res = await gmail_api.messages_list(user_id=email,
                                            labels_ids=labels_ids,
                                            next_page_token=next_page_token)
        if res:
            await gmail_response_topic.send(key=KeyBase(list_id=req.list_id),
                                            value=GmailResponseModel(
                                                action=req.action,
                                                payload=res,
                                                error=res.error
                                            ))

    async def _on_messages_get(self,
                               req: GmailRequestModel) -> Any:
        body = req.body
        if not body:
            raise AppErrors(f"_on_messages_get ERROR: body can't be empty for req={req}")

        email = body['account']
        if not email:
            raise AppErrors(f"_on_messages_get ERROR: account can't be empty for req={req}")


    def get_account(self, email):
        account = await self.account_service.get_by_email(email)
        if not account:
            raise AppErrors(f"there is no account found for {email}")

        return account