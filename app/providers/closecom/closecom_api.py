from app.exceptions import *
from typing import Any
from app.core.config import settings
import aiohttp
from aiohttp import BasicAuth
import traceback
import os
from app.core.config import settings

from app.schemas.models.closecom.sequence import *
from app.schemas.models.closecom.subscription import *
from app.schemas.models.closecom.lead import CloseComLeadChangeStatus, ApiLeadChangeStatus
from app.schemas.models.closecom.contactemail import ApiContactsGet

class CloseComApiProvider():
    def __init__(self, direct=True):
        if direct:
            raise AppErrors("Must use async create_api_provider to create instance")

        self.session = None

    @classmethod
    async def create_api_provider(cls,
                                  settings: dict=settings.CLOSECOM_API_SETTINGS) -> Any:

        api_provider = cls(direct=False)

        api_provider.api_settings = settings

        return api_provider

    async def get_client_session(self):
        if self.session:
            raise AppErrors("Session already created - use ONE session per app")

        api_key = self.api_settings['api_key']

        self.session = aiohttp.ClientSession(
            auth=BasicAuth(login=api_key, password='')
        )

        return self.session

    async def lead_change_status(self,
                                 payload: CloseComLeadChangeStatus,
                                 paginate=False,
                                 once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/lead/{payload.lead_id}/",
                                                 payload=ApiLeadChangeStatus(status_id=payload.status_id))

        return await self._dispatch(prepared_request=prepared_request,
                                    command='lead_change_status',
                                    req='PUT')

    async def list_lead_statuses(self,
                                 paginate=False,
                                 once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/status/lead/")

        if not paginate:
            return await self._dispatch(prepared_request=prepared_request,
                                        command='list_lead_statuses')

        return await self._paginate(prepared_request=prepared_request,
                                    command='list_lead_statuses')


    async def list_leads_by_query(self,
                                  query,
                                  paginate=False,
                                  once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/lead/")

        if not paginate:
            return await self._dispatch(prepared_request=prepared_request,
                                        command='list_leads_by_query',
                                        params={'query' : query})

        return await self._paginate(prepared_request=prepared_request,
                                    command='list_leads_by_query',
                                    params={'query' : query})


    async def list_emails(self,
                          payload,
                          paginate=True,
                          once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/activity/email/')

        params = payload.dict()
        return await self._paginate(prepared_request=prepared_request,
                                    command='list_emails',
                                    params=params,
                                    once=once)

    async def list_email_threads(self,
                                 payload,
                                 paginate=True,
                                 once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/activity/emailthread/')

        params = payload.dict()
        return await self._paginate(prepared_request=prepared_request,
                                    command='list_email_threads',
                                    params=params,
                                    once=once)


    async def list_activities(self,
                              paginate=False,
                              once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/activity/')

        return await self._dispatch(prepared_request=prepared_request,
                                    command='list_activities')

    async def list_accounts(self,
                            paginate=False,
                            once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/connected_account/')

        if not paginate:
            return await self._dispatch(prepared_request=prepared_request,
                                        command='list_accounts')

        return await self._paginate(prepared_request=prepared_request,
                                    command='list_accounts')

    async def list_sequence(self,
                            s_id,
                            paginate=False,
                            once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/sequence/{s_id}/")

        return await self._dispatch(prepared_request=prepared_request,
                                    command='list_sequence')


    async def list_sequences(self,
                             paginate=False,
                             once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/sequence/')

        if not paginate:
            return await self._dispatch(prepared_request=prepared_request,
                                        command='list_sequences')

        return await self._paginate(prepared_request=prepared_request,
                                    command='list_sequences')


    async def list_smartviews(self,
                              paginate=False,
                              once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/saved_search/')

        if not paginate:
            return await self._dispatch(prepared_request=prepared_request,
                                        command='list_smartviews')

        return await self._paginate(prepared_request=prepared_request,
                                    command='list_smartviews')


    async def list_bulk_active_sequences(self,
                                         paginate=False,
                                         once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/bulk_action/sequence_subscription/')

        return await self._dispatch(prepared_request=prepared_request,
                                    command='list_bulk_active_sequences')

    async def list_bulk_subscription(self,
                                     s_id,
                                     paginate=False,
                                     once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/bulk_action/sequence_subscription/{s_id}/")

        return await self._dispatch(prepared_request=prepared_request,
                                    command='list_bulk_subscription')

    async def list_subscriptions(self,
                                 paginate=False,
                                 once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/sequence_subscription/")

        if not paginate:
            return await self._dispatch(prepared_request=prepared_request,
                                        command='list_subscriptions')

        return await self._paginate(prepared_request=prepared_request,
                                    command='list_subscriptions')


    async def list_subscription(self,
                                s_id,
                                paginate=False,
                                once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/sequence_subscription/{s_id}/")

        return await self._dispatch(prepared_request=prepared_request,
                                    command='list_subscription')

    async def edit_subscription(self,
                                s_id,
                                payload: EditSubscription,
                                paginate=False,
                                once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name=f"/sequence_subscription/{s_id}/",
                                                 payload=payload)

        return await self._dispatch(prepared_request=prepared_request,
                                    command='edit_subscription',
                                    req='PUT')

    async def sequence_subscribe(self,
                                 payload: ApiSubscribeSequence,
                                 paginate=False,
                                 once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/sequence_subscription/',
                                                 payload=payload)

        return await self._dispatch(prepared_request=prepared_request,
                                    command='sequence_subscribe',
                                    req='POST')



    async def finish_subscription(self,
                                  s_id,
                                  paginate=False,
                                  once=False):
        payload = EditSubscription(status="paused")
        return await self.edit_subscription(s_id=s_id,
                                            payload=payload,
                                            paginate=paginate)


    async def bulk_start_sequence(self,
                                  payload: BulkStartSequence,
                                  paginate=False,
                                  once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/bulk_action/sequence_subscription/',
                                                 payload=payload)

        return await self._dispatch(prepared_request=prepared_request,
                                    command='bulk_start_sequence',
                                    req='POST')

    async def bulk_pause_sequence(self,
                                  payload: BulkPauseSequence,
                                  paginate=False,
                                  once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/bulk_action/sequence_subscription/',
                                                 payload=payload)

        return await self._dispatch(prepared_request=prepared_request,
                                    command='bulk_pause_sequence',
                                    req='POST')

    async def bulk_resume_sequence(self,
                                   payload: BulkResumeSequence,
                                   paginate=False,
                                   once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/bulk_action/sequence_subscription/',
                                                 payload=payload)

        return await self._dispatch(prepared_request=prepared_request,
                                    command='bulk_resume_sequence',
                                    req='POST')


    async def get_contacts(self,
                           payload: ApiContactsGet,
                           paginate=True,
                           once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/contact/')

        return await self._paginate(prepared_request=prepared_request,
                                    command='get_contacts',
                                    _skip=payload.skip,
                                    once=once)

    async def get_all_leads(self,
                           paginate=True,
                           once=False):
        if not self.session:
            raise AppErrors("Call get_client_session first")

        prepared_request = self._prepare_request(method_name='/lead/')

        return await self._paginate(prepared_request=prepared_request,
                                    command='get_all_leads',
                                    once=once)


    async def _paginate(self,
                        prepared_request,
                        command,
                        params=None,
                        _skip=0,
                        req='GET',
                        once=False):
        pages = []

        paginated_request = prepared_request
        if _skip:
            paginated_request = self._setup_shift(prepared_request,
                                                  _skip=_skip)

        while True:
            next_page = await self._dispatch(prepared_request=paginated_request,
                                             command=command,
                                             params=params,
                                             req=req)

            data = next_page.get('data', None)
            if not data:
                settings.LOGGER.error(f"There is no data in response for {command}")
                break

            received=len(data)
            settings.LOGGER.info(f"received={received} skip={_skip}  limit={settings.CLOSECOM_PAGE_LIMIT}")
            pages.extend(data)

            if once:
                settings.LOGGER.info(f"BREAK on once: once={once}")
                break

            has_more = next_page.get('has_more', False)
            if not has_more:
                break

            _skip = _skip + received
            paginated_request = self._paginate_request(prepared_request, _skip)

        return pages

    async def _dispatch(self,
                  prepared_request,
                  command,
                        params=None,
                        req='GET'):

        request = self.session.get
        if req == 'POST':
            request = self.session.post
        elif req == 'PUT':
            request = self.session.put
        elif req == 'DELETE':
            request = self.session.delete

        settings.LOGGER.debug(f"request = {prepared_request}")
        async with request(**prepared_request, params=params) as response:
            try:
                settings.LOGGER.debug(response.request_info)
                return await self._handle_response(response)
            except Exception as e:
                traceback.print_exc()
                settings.LOGGER.error(f"..{os.path.basename(__file__)} {command}  ERROR: {str(e)}")
                raise AppErrors(f"error executin command={command} error={str(e)}")

    def _setup_shift(self, prepared_request, _skip):
        url = prepared_request.get('url', None)
        if not url:
            raise Exception(f"Wrong prepared_request, not url ={prepared_request}")

        url = url + f"?_skip={_skip}&_limit={settings.CLOSECOM_PAGE_LIMIT}"

        paginated_request = prepared_request.copy()
        paginated_request['url'] = url

        return paginated_request


    def _paginate_request(self,
                          prepared_request,
                          _skip):
        url = prepared_request.get('url', None)
        if not url:
            raise Exception(f"Wrong prepared_request, not url ={prepared_request}")


        url = url + f"?_skip={_skip}&_limit={settings.CLOSECOM_PAGE_LIMIT}"

        paginated_request = prepared_request.copy()
        paginated_request['url'] = url

        return paginated_request

    def _prepare_request(self, method_name, payload=None, params=None, headers={}):
        request = {
            'url' : self.api_settings['base_url'] + method_name
        }

        if payload:
            headers.update({
                'Content-Type': 'application/json'
            })
            request["data"] = payload.json()
#           request["json"] = payload.json()


        request["headers"] = headers

        return request

    async def _handle_response(self, response: aiohttp.ClientResponse):
        if response.status == 429:
            wait_secs = self._get_rate_limit_sleep_time(response)
            raise AppErrors(f"CloseComApiProvider exceed rate limit need to wait for {wait_secs} and try again")

        if (response.status != 200) and (response.status != 201):
            content = await response.content.read()
            raise AppErrors(f"Error request status={response.status} content={content}")

        if response.status == 204:
            return ''

        response = await response.json()

        settings.LOGGER.debug(f"...response = {response}")
        return response

    def _get_rate_limit_sleep_time(self, response: aiohttp.ClientResponse):
        try:
            data = response.json()
            rate_reset = float(data['error']['rate_reset'])
            settings.LOGGER.info(f"..rate_limit reset in={rate_reset}")
            return rate_reset
        except (AttributeError, KeyError, ValueError):
            settings.LOGGER.info(f"..rate_limit reset in=10")
            return 10
