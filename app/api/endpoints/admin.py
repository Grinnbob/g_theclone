from typing import List, Any
from fastapi import APIRouter, Body, Depends, Path, Query, HTTPException, status, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from app.exceptions import *
from app.services import admin_dashboard_service as admin_service

import app.schemas.models.addon.template as template_schema
import app.schemas.models.addon.sequence as sequence_schema
import app.schemas.models.addon.test as test_schema
import app.schemas.models.admin as admin_schema
import app.schemas.models.closecom as closecom_schema

import app.schemas.models.user as user_schema
import app.schemas.models.account as account_schema

from app.schemas.auth import Token
from app.api import deps
from app.core.config import settings
from app.services.models.user import User
from app.api.auth import create_access_token
from app.api.utils import *

router = APIRouter()


@router.get("/templates/", response_model=List[template_schema.TemplateInDB])
async def get_templates(
    admin_user: User = Depends(deps.get_active_admin_user),
    service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.get_templates())



@router.get("/users/", response_model=List[user_schema.UserInDB])
async def get_users(
    admin_user: User = Depends(deps.get_active_admin_user),
    service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.get_users())



@router.get("/accounts/", response_model=List[account_schema.AccountInDB])
async def get_accounts(
    admin_user: User = Depends(deps.get_active_admin_user),
    service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.get_accounts())



@router.get("/sequences/", response_model=List[sequence_schema.SequnceInDB])
async def get_sequences(
    admin_user: User = Depends(deps.get_active_admin_user),
    service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.get_sequences())



@router.get("/tests/", response_model=List[test_schema.TestInDB])
async def get_tests(
    admin_user: User = Depends(deps.get_active_admin_user),
    service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.get_tests())


####################################################################################
######################## CHANGE   methods ##########################################
####################################################################################


######################## ACCOUNTS ##########################################
@router.put("/accounts/status/", response_model=account_schema.AccountInDB)
async def account_change_status(
    payload: admin_schema.AdmAccountChangeStatus,
    admin_user: User = Depends(deps.get_active_admin_user),
    service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:

    return hack_serialize(await service.change_account_status(account_id=payload.account_id,
                                                              active=payload.active))



@router.put("/accounts/connect/")
async def account_connect(
        payload: admin_schema.AdmAccountConnect,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.connect_account(account_id=payload.account_id,
                                                        user_id=payload.user_id))



@router.put("/accounts/disconnect/")
async def account_disconnect(
        payload: admin_schema.AdmAccountConnect,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.disconnect_account(account_id=payload.account_id,
                                                            user_id=payload.user_id))



######################## TEMPLATES ##########################################
@router.put("/templates/edit/")
async def template_edit(
        payload: admin_schema.AdmTemplateEdit,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.edit_template(template_id=payload.template_id,
                                                        data=payload.data))


@router.put("/templates/status/")
async def template_change_status(
        payload: admin_schema.AdmTemplateChangeStatus,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.change_template_status(template_id=payload.template_id,
                                                                active=payload.active))


@router.put("/templates/connect/")
async def template_connect(
        payload: admin_schema.AdmTemplateConnect,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.connect_template(template_id=payload.template_id,
                                                        account_ids=payload.account_ids,
                                                        to_all=payload.all))



@router.put("/templates/disconnect/")
async def template_disconnect(
        payload: admin_schema.AdmTemplateConnect,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.disconnect_template(template_id=payload.template_id,
                                                        account_ids=payload.account_ids,
                                                        from_all=payload.all))



######################## SEQUENCES ##########################################
@router.put("/sequences/edit/")
async def sequence_edit(
        payload: admin_schema.AdmSequenceEdit,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.edit_sequence(sequence_id=payload.sequence_id,
                                                        data=payload.data))



@router.put("/sequences/status/")
async def sequence_change_status(
        payload: admin_schema.AdmSequenceChangeStatus,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.change_sequence_status(sequence_id=payload.sequence_id,
                                                                active=payload.active))



######################## USERS ##########################################
@router.put("/users/level/")
async def user_change_level(
        payload: admin_schema.AdmUserChangeLevel,
        admin_user: User = Depends(deps.get_active_admin_user),
        service: admin_service.AdminDashboardService = Depends(deps.get_admin_service)
) -> Any:
    return hack_serialize(await service.change_user_level(user_id=payload.user_id,
                                                            level=payload.level))




######################## CLOSECOM ##########################################
from app.providers.closecom.closecom_api import CloseComApiProvider

async def _execute_closecom_api(api_name, payload=None):
    api_provider = await CloseComApiProvider.create_api_provider()

    api_session = await api_provider.get_client_session()
    async with api_session as session:
        api_method = getattr(api_provider, api_name)
        data = {}
        if payload:
            data = await api_method(payload)
        else:
            data = await api_method()

        json_compatible_item_data = jsonable_encoder(data)
        return JSONResponse(content=json_compatible_item_data)


@router.get("/closecom/accounts/")
async def closecom_list_accounts(
    admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('list_accounts')


@router.get("/closecom/sequences/")
async def closecom_list_sequences(
    admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('list_sequences')

@router.get("/closecom/smartviews/")
async def closecom_list_smartviews(
    admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('list_smartviews')


@router.get("/closecom/active_sequences/")
async def closecom_list_active_sequences(
    admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('list_bulk_active_sequences')


@router.put("/closecom/sequences/start/")
async def closecom_sequence_start(
        payload: closecom_schema.BulkStartSequence,
        admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('bulk_start_sequence', payload)

@router.put("/closecom/sequences/pause/")
async def closecom_sequence_pause(
        payload: closecom_schema.BulkPauseSequence,
        admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('bulk_pause_sequence', payload)

@router.put("/closecom/sequences/resume/")
async def closecom_sequence_resume(
        payload: closecom_schema.BulkResumeSequence,
        admin_user: User = Depends(deps.get_active_admin_user)
) -> Any:
    return await _execute_closecom_api('bulk_resume_sequence', payload)
